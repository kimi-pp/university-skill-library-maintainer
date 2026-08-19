---
name: fintech-developer
description: Specialized development skill for financial technology applications, including payment processing, financial calculations, compliance, security, and marketplace features specific to seller financing platforms like SellerFi.
author: SellerFin Team
license: MIT
---

# Fintech Developer

Comprehensive development skill for building secure, compliant, and scalable financial technology applications. Specializes in seller financing platforms, B2B marketplaces, payment processing, and financial data management.

## Core Fintech Domains

### 1. Payment Processing & Financial Transactions
- Payment gateway integration (Stripe, PayPal, Plaid)
- ACH transfers and wire transfers
- Escrow account management
- Multi-party payment splits
- Subscription billing and recurring payments
- Financial reconciliation and settlement
- PCI DSS compliance implementation

### 2. Financial Calculations & Modeling
- Seller financing terms calculation
- Interest rate computations
- Amortization schedules
- Cash flow projections
- ROI and IRR calculations
- Risk assessment algorithms
- Financial statement analysis

### 3. Compliance & Regulatory Requirements
- KYC (Know Your Customer) implementation
- AML (Anti-Money Laundering) checks
- GDPR and privacy compliance
- SOX compliance for financial data
- Bank Secrecy Act requirements
- State and federal lending regulations
- Financial audit trail maintenance

### 4. Security & Data Protection
- Financial data encryption (AES-256)
- Secure API design
- OAuth 2.0 and JWT implementation
- Multi-factor authentication
- Fraud detection systems
- Secure document handling
- HTTPS and certificate management

## SellerFi-Specific Features

### Business Marketplace Features
```typescript
// Business Listing Management
interface BusinessListing {
  id: string
  title: string
  description: string
  askingPrice: number
  revenue: number
  cashflow: number
  industry: string
  location: {
    city: string
    state: string
    showExact: boolean
  }
  financials: {
    revenue: number[]  // Last 3 years
    expenses: number[]
    netIncome: number[]
    askingPrice: number
    downPayment: number
    sellerFinancing: {
      amount: number
      rate: number
      term: number // months
    }
  }
  documents: SecureDocument[]
  status: 'draft' | 'active' | 'pending' | 'sold'
}

// Seller Financing Calculator
const calculateSellerFinancing = (
  askingPrice: number,
  downPayment: number,
  interestRate: number,
  termMonths: number
) => {
  const financeAmount = askingPrice - downPayment
  const monthlyRate = interestRate / 100 / 12
  const monthlyPayment = financeAmount *
    (monthlyRate * Math.pow(1 + monthlyRate, termMonths)) /
    (Math.pow(1 + monthlyRate, termMonths) - 1)

  return {
    financeAmount,
    monthlyPayment,
    totalInterest: (monthlyPayment * termMonths) - financeAmount,
    totalPayments: monthlyPayment * termMonths
  }
}
```

### Deal Room Management
```typescript
interface DealRoom {
  id: string
  listingId: string
  buyerId: string
  sellerId: string
  status: 'discovery' | 'nda_signed' | 'due_diligence' | 'loi_submitted' | 'under_contract' | 'closed'
  documents: {
    nda?: SecureDocument
    loi?: SecureDocument
    financials?: SecureDocument[]
    contracts?: SecureDocument[]
  }
  communications: Message[]
  timeline: DealTimelineEvent[]
  terms: {
    proposedPrice: number
    downPayment: number
    sellerFinancing: SellerFinancingTerms
    contingencies: string[]
  }
}

// Deal Progress Tracking
const updateDealStatus = async (
  dealRoomId: string,
  newStatus: DealStatus,
  userId: string
) => {
  // Validate state transition
  // Update database
  // Trigger notifications
  // Log audit trail
  // Update related documents
}
```

### Financial Due Diligence
```typescript
interface FinancialAnalysis {
  businessId: string
  revenue: {
    last3Years: number[]
    trend: 'increasing' | 'decreasing' | 'stable'
    seasonality: boolean
    recurring: number // percentage of recurring revenue
  }
  expenses: {
    categories: {
      cogs: number
      labor: number
      overhead: number
      marketing: number
    }
    fixedVsVariable: {
      fixed: number
      variable: number
    }
  }
  profitability: {
    grossMargin: number
    netMargin: number
    ebitda: number
    trends: FinancialTrend[]
  }
  risks: {
    customerConcentration: number
    supplierDependency: number
    marketRisk: 'low' | 'medium' | 'high'
    financialRisk: 'low' | 'medium' | 'high'
  }
}

const performFinancialAnalysis = (financials: BusinessFinancials): FinancialAnalysis => {
  // Complex financial analysis logic
  // Risk assessment algorithms
  // Trend analysis
  // Industry benchmarking
}
```

## Payment Integration Patterns

### Stripe Integration for B2B Payments
```typescript
import Stripe from 'stripe'

class PaymentService {
  private stripe: Stripe

  constructor() {
    this.stripe = new Stripe(process.env.STRIPE_SECRET_KEY!)
  }

  // Create escrow account for deal
  async createEscrowAccount(dealId: string, amount: number) {
    const paymentIntent = await this.stripe.paymentIntents.create({
      amount: amount * 100, // Convert to cents
      currency: 'usd',
      capture_method: 'manual', // Hold funds
      metadata: {
        dealId,
        type: 'escrow'
      }
    })
    return paymentIntent
  }

  // Multi-party payment split
  async processDealClosing(
    dealId: string,
    totalAmount: number,
    splits: PaymentSplit[]
  ) {
    const transfer = await this.stripe.transfers.create({
      amount: totalAmount * 100,
      currency: 'usd',
      destination: 'seller_account_id',
      metadata: { dealId }
    })

    // Process platform fee
    const platformFee = await this.stripe.transfers.create({
      amount: Math.round(totalAmount * 0.02 * 100), // 2% platform fee
      currency: 'usd',
      destination: 'platform_account_id'
    })

    return { transfer, platformFee }
  }
}
```

### Plaid Integration for Financial Verification
```typescript
import { PlaidApi, Configuration, PlaidEnvironments } from 'plaid'

class FinancialVerificationService {
  private plaidClient: PlaidApi

  constructor() {
    this.plaidClient = new PlaidApi(new Configuration({
      basePath: PlaidEnvironments[process.env.PLAID_ENV!],
      baseOptions: {
        headers: {
          'PLAID-CLIENT-ID': process.env.PLAID_CLIENT_ID!,
          'PLAID-SECRET': process.env.PLAID_SECRET!,
        },
      },
    }))
  }

  async verifyBusinessBankAccount(accessToken: string) {
    const accountsResponse = await this.plaidClient.accountsGet({
      access_token: accessToken
    })

    const transactionsResponse = await this.plaidClient.transactionsGet({
      access_token: accessToken,
      start_date: '2023-01-01',
      end_date: '2024-01-01'
    })

    return {
      accounts: accountsResponse.data.accounts,
      transactions: transactionsResponse.data.transactions,
      averageBalance: this.calculateAverageBalance(transactionsResponse.data.transactions),
      cashFlow: this.analyzeCashFlow(transactionsResponse.data.transactions)
    }
  }
}
```

## Database Schema Design

### Business Listings Schema
```sql
-- Businesses table
CREATE TABLE businesses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  seller_id UUID NOT NULL REFERENCES users(id),
  title VARCHAR(255) NOT NULL,
  description TEXT,
  industry VARCHAR(100),
  asking_price DECIMAL(15,2),
  revenue_last_year DECIMAL(15,2),
  net_income DECIMAL(15,2),
  location_city VARCHAR(100),
  location_state VARCHAR(2),
  location_precision location_precision_enum DEFAULT 'city',
  status listing_status_enum DEFAULT 'draft',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Financial records
CREATE TABLE business_financials (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  business_id UUID NOT NULL REFERENCES businesses(id),
  year INTEGER NOT NULL,
  revenue DECIMAL(15,2),
  cogs DECIMAL(15,2),
  gross_profit DECIMAL(15,2),
  operating_expenses DECIMAL(15,2),
  net_income DECIMAL(15,2),
  cash_flow DECIMAL(15,2),
  verified BOOLEAN DEFAULT FALSE,
  verification_date TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Deal rooms
CREATE TABLE deal_rooms (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  business_id UUID NOT NULL REFERENCES businesses(id),
  buyer_id UUID NOT NULL REFERENCES users(id),
  seller_id UUID NOT NULL REFERENCES users(id),
  status deal_status_enum DEFAULT 'discovery',
  proposed_price DECIMAL(15,2),
  down_payment DECIMAL(15,2),
  seller_carry_amount DECIMAL(15,2),
  seller_carry_rate DECIMAL(5,2),
  seller_carry_term INTEGER, -- months
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### Security & Compliance Features
```typescript
// Document encryption service
class SecureDocumentService {
  async uploadSecureDocument(
    file: File,
    dealRoomId: string,
    documentType: DocumentType,
    userId: string
  ) {
    // Encrypt file
    const encryptedBuffer = await this.encryptFile(file)

    // Generate secure URL
    const secureUrl = await this.uploadToSecureStorage(encryptedBuffer)

    // Log access
    await this.auditLog.log({
      action: 'document_upload',
      userId,
      dealRoomId,
      documentType,
      timestamp: new Date()
    })

    return {
      documentId: generateUUID(),
      secureUrl,
      metadata: {
        originalName: file.name,
        size: file.size,
        type: documentType,
        uploadedBy: userId,
        uploadedAt: new Date()
      }
    }
  }

  async accessSecureDocument(documentId: string, userId: string) {
    // Check permissions
    const hasAccess = await this.checkDocumentAccess(documentId, userId)
    if (!hasAccess) throw new UnauthorizedError()

    // Generate temporary access URL
    const tempUrl = await this.generateTemporaryUrl(documentId, 3600) // 1 hour

    // Log access
    await this.auditLog.log({
      action: 'document_access',
      userId,
      documentId,
      timestamp: new Date()
    })

    return tempUrl
  }
}
```

## Testing Strategies

### Financial Calculation Testing
```typescript
describe('Seller Financing Calculator', () => {
  test('calculates monthly payment correctly', () => {
    const result = calculateSellerFinancing(
      1000000, // $1M asking price
      200000,  // $200K down payment
      6.5,     // 6.5% interest rate
      120      // 10 years
    )

    expect(result.financeAmount).toBe(800000)
    expect(result.monthlyPayment).toBeCloseTo(9080.33, 2)
    expect(result.totalInterest).toBeCloseTo(289639.6, 2)
  })

  test('handles edge cases correctly', () => {
    // Test zero down payment
    // Test zero interest rate
    // Test very short/long terms
  })
})
```

### Security Testing
```typescript
describe('Security Features', () => {
  test('prevents unauthorized document access', async () => {
    const unauthorizedUser = 'user-123'
    const restrictedDocument = 'doc-456'

    await expect(
      secureDocumentService.accessSecureDocument(restrictedDocument, unauthorizedUser)
    ).rejects.toThrow(UnauthorizedError)
  })

  test('encrypts sensitive data', async () => {
    const sensitive = { ssn: '123-45-6789', bankAccount: '12345678' }
    const encrypted = await encryptionService.encrypt(sensitive)

    expect(encrypted).not.toContain('123-45-6789')
    expect(encrypted).not.toContain('12345678')
  })
})
```

## Performance & Scalability

### Database Optimization
```sql
-- Indexes for common queries
CREATE INDEX idx_businesses_industry_price ON businesses(industry, asking_price);
CREATE INDEX idx_deal_rooms_status ON deal_rooms(status);
CREATE INDEX idx_business_financials_year ON business_financials(business_id, year);

-- Partial indexes for active listings
CREATE INDEX idx_active_businesses ON businesses(created_at DESC)
WHERE status = 'active';
```

### Caching Strategy
```typescript
class BusinessSearchService {
  async searchBusinesses(filters: SearchFilters) {
    const cacheKey = `search:${JSON.stringify(filters)}`

    // Try cache first
    const cached = await this.redis.get(cacheKey)
    if (cached) return JSON.parse(cached)

    // Query database
    const results = await this.database.searchBusinesses(filters)

    // Cache for 5 minutes
    await this.redis.setex(cacheKey, 300, JSON.stringify(results))

    return results
  }
}
```

## Monitoring & Analytics

### Financial Metrics Dashboard
```typescript
interface PlatformMetrics {
  totalListings: number
  activeDeals: number
  totalTransactionVolume: number
  averageDealSize: number
  conversionRate: number
  platformRevenue: number
  topIndustries: IndustryMetric[]
  geographicDistribution: LocationMetric[]
}

class AnalyticsService {
  async generateDashboardMetrics(): Promise<PlatformMetrics> {
    const [
      totalListings,
      activeDeals,
      transactions,
      deals
    ] = await Promise.all([
      this.countTotalListings(),
      this.countActiveDeals(),
      this.getTotalTransactionVolume(),
      this.getCompletedDeals()
    ])

    return {
      totalListings,
      activeDeals,
      totalTransactionVolume: transactions.total,
      averageDealSize: transactions.total / deals.length,
      conversionRate: deals.length / totalListings,
      platformRevenue: transactions.total * 0.02, // 2% platform fee
      topIndustries: await this.getTopIndustries(),
      geographicDistribution: await this.getGeographicDistribution()
    }
  }
}
```

This fintech development skill provides comprehensive patterns and practices specifically tailored for building secure, compliant, and scalable seller financing platforms like SellerFi.