# Changelog

## 1.0.0

Initial standalone release of the portable Tunnlix Key core, extracted from the RP2350 firmware with relevant Git history preserved.

- Retains CTAP, CBOR, credential services, PIN protocols/policy and CTAPHID behavior.
- Keeps platform cryptography, persistent storage and transport behind callback interfaces.
- Makes the HID INIT product version an explicit integration setting, matching GetInfo/USB ownership. Standalone convenience handlers use 0.0.0 when no product version is supplied.
- Adds the `Tunnlix::KeyCore` CMake alias while preserving `ctap_core` and public include paths.
- Includes portable protocol checks and independent build/release packaging.

No persistent-data migration is introduced by this extraction. Firmware versioning, hardware providers, signing, OTP and recovery remain the responsibility of each platform integration. Existing firmware conformance results are not transferred to this release automatically.
