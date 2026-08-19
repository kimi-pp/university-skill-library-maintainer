---
name: cpp
description: Full C++ development aid with emphasis on memory safety and cross-platform programming. Use when the user wants to create, edit, build, run, debug, or test C++ source files, headers, or CMake projects. Scaffolds files with proper headers, enforces modern C++ best practices, memory-safe idioms, cross-platform CMake builds, and assists with debugging and testing.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
argument-hint: [action or filename]
---

# C++ Development Skill (Memory-Safe, Cross-Platform)

Assist with all aspects of modern C++ development with a strong emphasis on memory safety and cross-platform portability. This includes creating files, writing code, building projects, running executables, debugging, and testing.

## Creating New Files

When creating a new C++ source file (`.cpp`) or header (`.hpp`/`.h`), always include the file header from CLAUDE.md using the `/* */` comment template (C, C++, Objective-C, Swift style).

### Source file template (.cpp):

```cpp
/*****************************************************************************************
 * example.cpp
 *
 * brief summary of the file contents
 *
 * Author   :  Gary Ash <gary.ash@icloud.com>
 * Created  :  <current date/time>
 * Modified :
 *
 * Copyright © <year> By Gary Ash All rights reserved.
 ****************************************************************************************/

#include "example.hpp"
```

### Header file template (.hpp):

```cpp
/*****************************************************************************************
 * example.hpp
 *
 * brief summary of the file contents
 *
 * Author   :  Gary Ash <gary.ash@icloud.com>
 * Created  :  <current date/time>
 * Modified :
 *
 * Copyright © <year> By Gary Ash All rights reserved.
 ****************************************************************************************/
#pragma once
```

Prefer `.hpp`/`.cpp` extensions for C++ files. Use `#pragma once` instead of `#ifndef` include guards.

## C++ Standard

- Target **C++20** as the default standard unless the project specifies otherwise
- Use C++23 features only when the project explicitly opts in
- Set the standard in CMake: `set(CMAKE_CXX_STANDARD 20)` with `set(CMAKE_CXX_STANDARD_REQUIRED ON)`

## Memory Safety (Critical)

Memory safety is the top priority. Apply these rules strictly:

### Ownership and Lifetime

- **Never use raw `new`/`delete`** — use smart pointers or containers instead
- **`std::unique_ptr`** for single-owner resources (default choice)
- **`std::shared_ptr`** only when shared ownership is genuinely needed
- **`std::weak_ptr`** to break reference cycles with `shared_ptr`
- Use **`std::make_unique`** and **`std::make_shared`** — never construct smart pointers from raw `new`
- Apply **RAII** (Resource Acquisition Is Initialization) for all resource management: files, locks, sockets, handles

### Containers and References

- Use **`std::vector`**, **`std::array`**, **`std::string`**, **`std::string_view`** instead of raw arrays and C strings
- Use **`std::span`** (C++20) for non-owning views over contiguous data
- Use **`std::optional`** instead of nullable raw pointers for optional values
- Use **`std::variant`** instead of unions
- Prefer **references** over pointers when null is not a valid state
- Prefer **`const&`** for read-only access to non-trivial types

### Array and Buffer Safety

- Use **`.at()`** for bounds-checked access during development/debug builds
- Use **`std::ranges`** algorithms instead of raw pointer iteration
- Never perform pointer arithmetic on raw pointers — use `std::span` or iterators
- Always validate sizes before buffer operations

### Concurrency Safety

- Use **`std::mutex`** with **`std::lock_guard`** or **`std::scoped_lock`** — never manual lock/unlock
- Use **`std::atomic`** for lock-free shared state
- Use **`std::jthread`** (C++20) over `std::thread` for automatic joining
- Prefer **`std::async`** / **`std::future`** for simple parallelism

### Error Handling

- Use **exceptions** for exceptional conditions or **`std::expected`** (C++23) / **`std::optional`** for expected failures
- Never ignore return values — use `[[nodiscard]]` on functions whose return value must be checked
- Avoid **`std::terminate`** / **`std::abort`** in library code
- Use **`static_assert`** for compile-time invariants

### Casts and Type Safety

- **Never use C-style casts** — use `static_cast`, `dynamic_cast`, `const_cast`, or `reinterpret_cast`
- Minimize use of `reinterpret_cast` and `const_cast` — both are code smells
- Use **`enum class`** instead of plain `enum`
- Use **`std::byte`** for raw byte manipulation instead of `char*` or `unsigned char*`

## Cross-Platform Development (Critical)

### CMake (Required Build System)

Always use CMake for cross-platform builds. Minimum CMakeLists.txt:

```cmake
cmake_minimum_required(VERSION 3.20)
project(ProjectName LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

add_executable(${PROJECT_NAME} src/main.cpp)
target_include_directories(${PROJECT_NAME} PRIVATE include)
```

Key CMake practices:
- Always set `CMAKE_CXX_EXTENSIONS OFF` to disable compiler-specific extensions
- Use `target_*` commands instead of global `include_directories()` or `add_definitions()`
- Use `FetchContent` or `find_package` for dependencies
- Export `compile_commands.json` for tooling: `set(CMAKE_EXPORT_COMPILE_COMMANDS ON)`

### Platform Abstraction

- Use **`std::filesystem`** for all path and file operations (not POSIX or Win32 APIs)
- Use **`std::chrono`** for all time operations
- Use **`<cstdint>`** fixed-width types: `int32_t`, `uint64_t`, `size_t`, `ptrdiff_t`
- Use **`std::thread`** / **`std::jthread`** for threading (not pthreads or Win32 threads)
- Use **`std::format`** (C++20) for string formatting
- Avoid platform-specific headers (`<windows.h>`, `<unistd.h>`) unless isolated behind abstractions

### When Platform-Specific Code Is Needed

```cpp
#if defined(_WIN32)
    // Windows-specific code
#elif defined(__APPLE__)
    // macOS/iOS-specific code
#elif defined(__linux__)
    // Linux-specific code
#else
    #error "Unsupported platform"
#endif
```

Isolate platform-specific code into dedicated source files with a common interface header.

### Portability Rules

- Never assume endianness — use `std::endian` (C++20) and `std::byteswap` (C++23) when needed
- Never assume `sizeof(int)` or pointer sizes — use fixed-width types
- Avoid compiler-specific attributes — use C++ standard `[[attributes]]`
- Use `std::source_location` (C++20) instead of `__FILE__`/`__LINE__` macros
- Avoid `#pragma` directives other than `#pragma once`

## Building and Running

### Building with CMake

```bash
cmake -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build
```

Build types:
- **Debug**: `-DCMAKE_BUILD_TYPE=Debug` — full debug info, no optimization
- **Release**: `-DCMAKE_BUILD_TYPE=Release` — optimized, no debug info
- **RelWithDebInfo**: `-DCMAKE_BUILD_TYPE=RelWithDebInfo` — optimized with debug info
- **ASAN build**: add `-DCMAKE_CXX_FLAGS="-fsanitize=address -fno-omit-frame-pointer"` and `-DCMAKE_EXE_LINKER_FLAGS="-fsanitize=address"`

### Running

```bash
./build/ProjectName
```

### Sanitizer Builds (Essential for Memory Safety)

Add a CMake option for sanitizers:

```cmake
option(ENABLE_SANITIZERS "Enable ASan and UBSan" OFF)
if(ENABLE_SANITIZERS)
    add_compile_options(-fsanitize=address,undefined -fno-omit-frame-pointer)
    add_link_options(-fsanitize=address,undefined)
endif()
```

Build with sanitizers:

```bash
cmake -B build-asan -DENABLE_SANITIZERS=ON -DCMAKE_BUILD_TYPE=Debug
cmake --build build-asan
```

Available sanitizers (Clang/GCC):
- **AddressSanitizer (ASan)**: `-fsanitize=address` — buffer overflows, use-after-free, memory leaks
- **UndefinedBehaviorSanitizer (UBSan)**: `-fsanitize=undefined` — signed overflow, null dereference, alignment
- **ThreadSanitizer (TSan)**: `-fsanitize=thread` — data races (cannot combine with ASan)
- **MemorySanitizer (MSan)**: `-fsanitize=memory` — uninitialized reads (Clang only, cannot combine with ASan)

Always run the test suite under ASan+UBSan before considering code complete.

## Code Quality

### Modern C++ Idioms

- Use structured bindings: `auto [key, value] = *map.begin();`
- Use `if constexpr` for compile-time branching
- Use concepts (C++20) to constrain templates
- Use `auto` for complex types but be explicit for readability at interfaces
- Use `constexpr` and `consteval` aggressively for compile-time computation
- Use designated initializers (C++20): `Point{.x = 1, .y = 2}`
- Use range-based `for` with structured bindings: `for (const auto& [k, v] : map)`
- Mark single-argument constructors `explicit`
- Follow the **Rule of Zero**: rely on compiler-generated special members by using smart pointers and standard containers
- If you must define one special member function, follow the **Rule of Five**

### Naming Conventions

- `PascalCase` for types and classes
- `snake_case` for functions, variables, and namespaces
- `UPPER_SNAKE_CASE` for constants and macros
- `m_` prefix for private member variables
- Avoid Hungarian notation

### Header Hygiene

- Include what you use — do not rely on transitive includes
- Use forward declarations where possible to reduce compile times
- Order includes: own header first, project headers, third-party headers, standard library
- Keep headers self-contained (every header compiles on its own)

## Debugging

### LLDB (primary on macOS)

- Launch: `lldb ./build/ProjectName`
- Key commands:
  - `r` (run), `n` (next), `s` (step into), `c` (continue), `finish` (step out)
  - `b <function>` or `b <file>:<line>` (set breakpoint)
  - `br list` (list breakpoints), `br del <n>` (delete breakpoint)
  - `p <expr>` (print), `po <expr>` (print object/formatted)
  - `bt` (backtrace), `frame variable` (show locals)
  - `watchpoint set variable <var>` (data breakpoint)
  - `q` (quit)

### GDB (primary on Linux)

- Launch: `gdb ./build/ProjectName`
- Key commands:
  - `r` (run), `n` (next), `s` (step into), `c` (continue), `finish` (step out)
  - `b <function>` or `b <file>:<line>` (set breakpoint)
  - `info b` (list breakpoints), `d <n>` (delete breakpoint)
  - `p <expr>` (print), `bt` (backtrace), `info locals`
  - `watch <expr>` (data breakpoint)
  - `q` (quit)

### Valgrind (Linux)

- Memory error detection: `valgrind --leak-check=full ./build/ProjectName`
- Detailed: `valgrind --leak-check=full --show-leak-kinds=all --track-origins=yes ./build/ProjectName`

## Static Analysis

### clang-tidy

- Run: `clang-tidy src/*.cpp -- -std=c++20 -Iinclude`
- With compile_commands.json: `clang-tidy -p build src/*.cpp`
- Fix in place: `clang-tidy -fix -p build src/*.cpp`
- Key check categories:
  - `cppcoreguidelines-*` — C++ Core Guidelines compliance
  - `modernize-*` — modernize legacy code
  - `bugprone-*` — common bug patterns
  - `performance-*` — performance improvements
  - `readability-*` — readability improvements
- Configure via `.clang-tidy` file in project root:
  ```yaml
  Checks: >
    -*,
    bugprone-*,
    cppcoreguidelines-*,
    modernize-*,
    performance-*,
    readability-*
  WarningsAsErrors: 'bugprone-*'
  ```

### cppcheck

- Run: `cppcheck --enable=all --std=c++20 --suppress=missingIncludeSystem src/`
- Check a single file: `cppcheck --enable=all --std=c++20 src/file.cpp`

### Compiler Warnings (Always Enable)

Add to CMakeLists.txt:

```cmake
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang|GNU")
    target_compile_options(${PROJECT_NAME} PRIVATE
        -Wall -Wextra -Wpedantic -Werror
        -Wconversion -Wsign-conversion
        -Wnon-virtual-dtor -Wold-style-cast
        -Wcast-align -Wunused -Woverloaded-virtual
        -Wshadow -Wnull-dereference
        -Wdouble-promotion -Wformat=2
        -Wimplicit-fallthrough
    )
elseif(MSVC)
    target_compile_options(${PROJECT_NAME} PRIVATE
        /W4 /WX /permissive-
        /w14640 /w14826 /w14928
    )
endif()
```

## Testing

### Google Test (recommended)

Add via CMake FetchContent:

```cmake
include(FetchContent)
FetchContent_Declare(
    googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG        v1.15.2
)
FetchContent_MakeAvailable(googletest)

enable_testing()
add_executable(tests tests/test_main.cpp)
target_link_libraries(tests PRIVATE GTest::gtest_main)
include(GoogleTest)
gtest_discover_tests(tests)
```

Test file structure:

```cpp
#include <gtest/gtest.h>
#include "my_module.hpp"

TEST(MyModuleTest, BasicOperation) {
    auto result = my_function(1, 2);
    EXPECT_EQ(result, 3);
}

TEST(MyModuleTest, EdgeCase) {
    EXPECT_THROW(my_function(-1, 0), std::invalid_argument);
}

TEST(MyModuleTest, NoLeaks) {
    auto ptr = create_resource();
    ASSERT_NE(ptr, nullptr);
    // unique_ptr ensures cleanup — no manual delete needed
}
```

Run tests:

```bash
cmake --build build
ctest --test-dir build --output-on-failure
```

### Catch2 (alternative)

```cmake
FetchContent_Declare(
    Catch2
    GIT_REPOSITORY https://github.com/catchorg/Catch2.git
    GIT_TAG        v3.7.1
)
FetchContent_MakeAvailable(Catch2)

add_executable(tests tests/test_main.cpp)
target_link_libraries(tests PRIVATE Catch2::Catch2WithMain)
```

## Common Cross-Platform Dependency Management

### FetchContent (preferred for small deps)

```cmake
FetchContent_Declare(
    fmt
    GIT_REPOSITORY https://github.com/fmtlib/fmt.git
    GIT_TAG        11.1.4
)
FetchContent_MakeAvailable(fmt)
target_link_libraries(${PROJECT_NAME} PRIVATE fmt::fmt)
```

### vcpkg

```bash
vcpkg install fmt nlohmann-json
cmake -B build -DCMAKE_TOOLCHAIN_FILE=$VCPKG_ROOT/scripts/buildsystems/vcpkg.cmake
```

### Conan

```bash
conan install . --build=missing
cmake -B build -DCMAKE_TOOLCHAIN_FILE=build/conan_toolchain.cmake
```

## Argument Handling

- If `$ARGUMENTS` is a filename ending in `.cpp`, `.hpp`, `.h`, or `.cc`, work with that file
- If `$ARGUMENTS` is "new <filename>", scaffold a new file with proper headers
- If `$ARGUMENTS` is "build", configure and build the CMake project
- If `$ARGUMENTS` is "run", build and run the project executable
- If `$ARGUMENTS` is "test", build and run the test suite
- If `$ARGUMENTS` is "check", run clang-tidy and cppcheck on the source tree
- If `$ARGUMENTS` is "sanitize", build with ASan+UBSan and run the test suite
- Otherwise, treat `$ARGUMENTS` as a general C++ development request
