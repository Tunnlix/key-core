# Integration contracts

Link `Tunnlix::KeyCore` and supply the interfaces declared in the public headers. The implementation does not supply a cryptographic library, hardware drivers or a persistent record format.

## Build configuration

Set cache options before adding the core. `CTAP_PIN_COMPLEXITY`, `CTAP_MESSAGE_CAPACITY`, `CTAP_RESIDENT_CAPACITY` and `CTAP_TOUCH_TIMEOUT_MS` affect behavior or structure sizes. Use the core target's PUBLIC compile definitions in every provider and application translation unit; do not compile different copies of a public structure with different settings. Keep separate build directories for different profiles.

`CTAP_EXPERIMENTAL_PIN2_OVERSIZE_POLICY` is an existing development compatibility experiment, OFF by default. It changes a malformed protocol-2 setPIN error response. It is not part of the ordinary protocol profile and must be recorded explicitly when enabled.

The core release version identifies the library. The application supplies firmware version, AAGUID, USB identity, transport declaration and product policies. These are not derived from the library version.

## Providers and lifetime

- `AuthCrypto` provides secure random generation, SHA-256 and opaque credential-key operations. `AuthSecretCrypto` provides key agreement and symmetric operations. Crypto providers validate curve inputs, implement secret-independent cryptographic operations where required and erase their own secret scratch. The core erases the transient buffers it owns.
- `AuthStorage` implements credential metadata operations. `AuthPinStorage` persists PIN/policy state. The application also supplies the relevant blob-store, reset, nonresident credential and attestation providers. Optional callback groups must be complete before their features are advertised.
- Callback contexts and state are application-owned and must outlive all references to them. Calls are serial, bounded and non-reentrant. The core supplies no scheduler, mutexes or interrupt synchronization.
- Storage callbacks report success only after required atomic durable state is committed. Lookup exhaustion uses NOT_FOUND; corruption and failed writes fail closed. Do not serialize native public C structures directly to flash. Reset must coordinate credential keys, metadata, PIN state and related privacy identifiers.
- Key handles are opaque, provider-specific locators. They must not be reused after deletion/reset. Switching a crypto provider is not a migration of stored keys.

The public header comments define the individual callback contracts, output lengths and failure behavior. Integration code must preserve these requirements when adapting to hardware accelerators, secure elements or a different storage medium.

## USB and asynchronous operations

The application supplies monotonic millisecond time, user-presence sampling and USB HID report submission/completion. CTAPHID owns channel and transaction state. The transport must preserve report sizes/order and acknowledge asynchronous transfers with their assigned transfer IDs. Backend results, cancellation and keepalive updates must retain their operation IDs so stale completions cannot finish another transaction.

The application owns polling and watchdog policy. Clock wrap is supported by the protocol state machines; board clock conversion must preserve their unsigned millisecond semantics. Coordinate interrupt/DMA activity outside the core and do not reenter callbacks.

## Persistence and security

The core does not implement MCU secure boot, OTP programming, firmware update authorization or hardware key isolation. The platform supplies those mechanisms. Changing a core API, a persistent format or a provider key derivation are separate compatibility decisions. A previous core release does not guarantee that an older firmware image can read newer stored data safely.

Persistent policies must not be silently weakened during an update or downgrade. Validate the complete integration, including power interruption, timing and reset behavior, on its actual hardware. Portable checks do not establish hardware conformance or certification.
