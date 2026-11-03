# Tunnlix Key Core

Portable C17 implementation of Tunnlix Key's CTAP authenticator and USB HID protocol state machines. Applications supply cryptography, persistent storage, user presence, time and transport callbacks.

The core contains CTAP command handling, CBOR encoding/decoding, PIN protocols and policy, credential services, extension handling, and CTAPHID framing/channel/transaction management. It has no Pico SDK, USB driver, flash driver or cryptographic library dependency.

A complete authenticator requires platform providers. Supported features are advertised according to the providers configured by the application. See [integration](docs/integration.md) for the provider contracts and [releases](docs/releases.md) for dependency and compatibility policy.

## Available hardware

Use an existing hardware integration to build a complete Tunnlix Key:

| Board | Microcontroller | Firmware and setup |
| --- | --- | --- |
| Seeed Studio XIAO RP2350 | Raspberry Pi RP2350 | [Firmware](https://github.com/Tunnlix/key-rp2350) · [Build and setup](https://github.com/Tunnlix/key-rp2350/blob/main/docs/building.md) |

The XIAO reference setup uses an external user-presence button between D0 and GND.

## Bring your own hardware

Contributions that bring Tunnlix Key to more boards and microcontrollers are
welcome. Reuse the protocol core and supply your platform's USB transport,
cryptography, persistent storage, random generation and user-presence controls.
Share what you are building and help expand the available hardware integrations.

Start with the [integration guide](docs/integration.md). Hardware drivers, firmware
updates, provisioning and secure boot belong to each platform's firmware project.

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
