---
name: distributed-logging-correlation
description: "Use when implementing structured logging with correlation IDs across service boundaries, diagnosing requests that cannot be traced end-to-end across services, or when log messages use string interpolation causing allocations on every call. Covers LoggerMessage source generator for zero-allocation logging, correlation ID middleware, W3C trace context propagation via Activity, OpenTelemetry integration, log scope context, and PII scrubbing rules. Domain: Observability, Logging, Tracing. Level: Intermediate. Tags: logging, correlation-id, opentelemetry, structured-logging, tracing."
---

# Distributed Logging & Correlation IDs

## Problem

Without structured logging and trace correlation:
- Logs are unstructured strings that can't be queried or filtered
- Requests spanning multiple services can't be traced end-to-end
- Performance issues require manual log archaeology across servers
- Log messages use string interpolation, allocating on every call regardless of log level
- Sensitive data leaks into log storage without awareness

## Solution: Structured Logging + Correlation IDs + OpenTelemetry

Combine high-performance structured logging with `Activity`-based trace propagation for end-to-end observability across services.

## Implementation

### Tier 1: High-Performance Structured Logging

#### LoggerMessage Source Generator (.NET 6+)

```csharp
public static partial class LogMessages
{
    [LoggerMessage(Level = LogLevel.Information, Message = "Order {OrderId} placed by customer {CustomerId}")]
    public static partial void OrderPlaced(ILogger logger, int orderId, int customerId);

    [LoggerMessage(Level = LogLevel.Warning, Message = "Retry attempt {Attempt} for order {OrderId}")]
    public static partial void RetryAttempt(ILogger logger, int attempt, int orderId);

    [LoggerMessage(Level = LogLevel.Error, Message = "Failed to process order {OrderId}")]
    public static partial void OrderProcessingFailed(ILogger logger, int orderId, Exception exception);
}
```

#### Usage

```csharp
public class OrderService
{
    private readonly ILogger<OrderService> _logger;

    public async Task PlaceOrderAsync(Order order, CancellationToken ct)
    {
        LogMessages.OrderPlaced(_logger, order.Id, order.CustomerId);
        // ... business logic
    }
}
```

### Tier 2: Correlation IDs

#### Middleware for Correlation Propagation

```csharp
public class CorrelationIdMiddleware
{
    private const string CorrelationHeader = "X-Correlation-Id";
    private readonly RequestDelegate _next;

    public CorrelationIdMiddleware(RequestDelegate next) => _next = next;

    public async Task InvokeAsync(HttpContext context)
    {
        var correlationId = context.Request.Headers[CorrelationHeader].FirstOrDefault()
            ?? Activity.Current?.Id
            ?? Guid.NewGuid().ToString();

        context.Response.Headers[CorrelationHeader] = correlationId;

        using (_logger.BeginScope(new Dictionary<string, object>
        {
            ["CorrelationId"] = correlationId
        }))
        {
            await _next(context);
        }
    }
}
```

#### Propagate to Outgoing HTTP Calls

```csharp
public class CorrelationDelegatingHandler : DelegatingHandler
{
    protected override async Task<HttpResponseMessage> SendAsync(
        HttpRequestMessage request, CancellationToken ct)
    {
        if (Activity.Current is not null)
        {
            request.Headers.TryAddWithoutValidation("X-Correlation-Id", Activity.Current.Id);
        }

        return await base.SendAsync(request, ct);
    }
}
```

### Tier 3: OpenTelemetry Integration

#### Configuration

```csharp
builder.Services.AddOpenTelemetry()
    .WithTracing(tracing => tracing
        .SetResourceBuilder(ResourceBuilder.CreateDefault()
            .AddService("OrderService"))
        .AddAspNetCoreInstrumentation()
        .AddHttpClientInstrumentation()
        .AddSqlClientInstrumentation(o => o.SetDbStatementForText = true)
        .AddOtlpExporter())
    .WithMetrics(metrics => metrics
        .AddAspNetCoreInstrumentation()
        .AddHttpClientInstrumentation()
        .AddOtlpExporter());
```

#### Custom Activity Source

```csharp
public static class Telemetry
{
    public static readonly ActivitySource Source = new("OrderService");
}

// Usage
using var activity = Telemetry.Source.StartActivity("ProcessOrder");
activity?.SetTag("order.id", orderId);
activity?.SetTag("order.total", total);
```

### Log Scopes for Context

```csharp
public async Task ProcessOrderAsync(int orderId, CancellationToken ct)
{
    using var scope = _logger.BeginScope(new Dictionary<string, object>
    {
        ["OrderId"] = orderId,
        ["Operation"] = "ProcessOrder"
    });

    LogMessages.OrderProcessingStarted(_logger, orderId);
    // All log messages within this scope include OrderId and Operation
}
```

## When to Use

- **Always.** Every service that runs in production should have structured logging and correlation.
- Multi-service architectures (microservices, distributed monolith) — correlation IDs are essential.
- Performance-sensitive code — use `LoggerMessage` source generator to avoid allocation.

## When NOT to Use

- Console applications or CLI tools with simple `Console.WriteLine` output (but even then, `ILogger` is better).
- Unit tests (mock `ILogger<T>` instead).

## Gotchas

1. **String interpolation in log calls**: `_logger.LogInformation($"Order {orderId}")` allocates a string on EVERY call, even when the log level is disabled. Use `LoggerMessage` or structured parameters: `_logger.LogInformation("Order {OrderId}", orderId)`.
2. **PII in logs**: Never log passwords, tokens, full credit card numbers, SSNs, or email addresses without masking. Use a log scrubber or mask at the source.
3. **Missing scopes**: Without `BeginScope`, log messages lack context. Add correlation ID, request ID, and operation name to every scope.
4. **Log level in production**: Use `Warning` as the minimum in production. `Information` is acceptable for key business events. Never leave `Debug` or `Trace` enabled in production.
5. **Activity.Current is null**: If no `ActivitySource` is configured or no listener is active, `Activity.Current` will be `null`. Always null-check before using.
6. **Over-logging**: Logging every method entry/exit at `Information` level creates noise and storage costs. Log business events, not implementation details.

## Exception Formatting Chain

Exceptions with nested `InnerException` chains lose context when only the top-level `Message` is logged.

### Formatter Implementation

```csharp
public static class ExceptionFormatter
{
    /// <summary>Formats the full exception chain into a single readable string.</summary>
    public static string Format(Exception exception, bool includeStackTrace = false)
    {
        var messages = new List<string> { exception.Message };

        var inner = exception.InnerException;
        while (inner is not null)
        {
            messages.Add($"Inner: {inner.Message}");
            inner = inner.InnerException;
        }

        var formatted = string.Join(" | ", messages);

        if (includeStackTrace && !string.IsNullOrWhiteSpace(exception.StackTrace))
            formatted += $" | StackTrace: {exception.StackTrace}";

        return formatted;
    }

    /// <summary>Extracts just the root cause message (deepest InnerException).</summary>
    public static string GetRootCauseMessage(Exception exception)
    {
        var current = exception;
        while (current.InnerException is not null)
            current = current.InnerException;
        return current.Message;
    }
}
```

### Output Example
```
Connection timeout expired | Inner: A connection attempt failed | Inner: No such host is known
```

- Always walk the full chain — root causes are in the deepest `InnerException`.
- Use `" | "` as separator for single-line log compatibility.
- Stack trace inclusion should be configurable (off by default in production).
- Consider `AggregateException.Flatten()` for `Task`-related exceptions.

## Fire-and-Forget Error Logging

Error handlers that synchronously write to file or network loggers can throw their own exceptions, masking the original error.

### Pattern

Log exceptions asynchronously with `_ = LogAsync(...)` (fire-and-forget) and swallow all logging failures. An error handler must never throw.

```csharp
public static class ErrorLogger
{
    /// <summary>Logs exception to file asynchronously. Non-blocking, never throws.</summary>
    public static async Task LogToFileAsync(string context, Exception exception, string? logPath = null)
    {
        try
        {
            var timestamp = DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss.fff");
            var message = $"[{timestamp}] [{context}] {ExceptionFormatter.Format(exception)}";
            var path = logPath ?? Path.Combine(
                AppDomain.CurrentDomain.BaseDirectory, "logs", "errors.log");
            var directory = Path.GetDirectoryName(path);
            if (directory is not null) Directory.CreateDirectory(directory);
            await File.AppendAllTextAsync(path, message + Environment.NewLine)
                .ConfigureAwait(false);
        }
        catch
        {
            // Swallow ALL logging errors — never throw from an error handler
        }
    }
}

// Usage: _ = ErrorLogger.LogToFileAsync(context, exception);
```

- **Never `await`** the fire-and-forget call in the error handler — use discard `_ =`.
- File logging is a *secondary* mechanism — the primary error recording must be synchronous and reliable.
- Consider log rotation or max file size limits for production use.
- **Not suitable** when logging failure is a business-critical event (financial audit trails).

## Related Skills

- Exponential Backoff with Jitter (retry logging with attempt counts)
- Retry with Exponential Backoff (retry logging with attempt counts)
- Multi-Stage CI/CD Pipeline (log aggregation in deployment pipeline)
- Health Check Endpoint (correlate health probe results with logs)
