# Tunnlix Key Core

Portable C17 implementation of Tunnlix Key's CTAP authenticator and USB HID protocol state machines. Applications supply cryptography, persistent storage, user presence, time and transport callbacks.

The core contains CTAP command handling, CBOR encoding/decoding, PIN protocols and policy, credential services, extension handling, and CTAPHID framing/channel/transaction management. It has no Pico SDK, USB driver, flash driver or cryptographic library dependency.

A complete authenticator requires platform providers. Supported features are advertised according to the providers configured by the application. See [integration](docs/integration.md) for the provider contracts and [releases](docs/releases.md) for dependency and compatibility policy.

## Build

```sh
cmake -S . -B build/core -DCMAKE_BUILD_TYPE=Release
cmake --build build/core
ctest --test-dir build/core --output-on-failure
```

Consumers can add the selected release with CMake `FetchContent` or `add_subdirectory()` and link `Tunnlix::KeyCore` (`ctap_core` remains available). Public headers retain their `authenticator/`, `ctap/` and `protocol/` paths.

`CTAP_PIN_COMPLEXITY` is enabled by default. Configure it and capacity overrides before adding the core. Public compile definitions propagate to consumers so provider structures use the same configuration. Standalone builds enable portable checks; embedded consumers can opt in with `KEY_CORE_BUILD_TESTS=ON`.

Board firmware, secure boot, provisioning, attestation identities and persistent-media formats belong to the integration. [Tunnlix Key for RP2350](https://github.com/Tunnlix/key-rp2350) supplies the first implementation. Conformance results apply to the complete tested firmware and configuration, rather than to this library alone.

MIT licensed. The initial extraction preserves relevant history from `Tunnlix/key-rp2350`; product firmware versioning is maintained by that repository.
