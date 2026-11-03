# Releases and compatibility

Core and firmware releases are independent. A platform-only firmware change can retain its existing core dependency. A new core release is adopted by an explicit firmware change after reviewing its effects on that platform.

Use semantic versioning: major for breaking public-interface or integration-contract changes, minor for compatible additions, patch for compatible fixes. Describe security-sensitive behavior, capacity/memory changes and storage consequences in release notes even when the public API remains compatible. No binary ABI compatibility across toolchains or different capacity/feature configurations is promised; rebuild the core and providers together.

Release tags and source assets are immutable. Never move an existing release tag or replace an asset with different bytes. Publish a new version to correct an error. Consumers select a named release and verify its exact source archive with SHA-256. They must not follow a moving branch or automatically adopt the latest release.

## Preparing a release

1. Review the core changes, standalone checks and at least the affected platform integration. Record the source commit and release version.
2. Set the CMake project version and changelog, then create an annotated `vMAJOR.MINOR.PATCH` tag on the reviewed commit.
3. Run `python3 tools/package-release.py --tag vMAJOR.MINOR.PATCH --output /path/to/artifacts` from the tagged checkout. It requires a clean tracked tree and emits a source archive, checksum and provenance record.
4. Build and run checks from the archive itself, including supported feature profiles.
5. Publish the release assets. The manual GitHub workflow prepares a draft release for review; publishing is a separate action.
6. Update a firmware consumer's release, source revision and archive checksum together. Retain its build profile and validation evidence.

An explicit local-source override is appropriate during coordinated development. Record that override in the build evidence; it is not a published release dependency. Release builds should consume the verified source archive.

The first extracted release preserves portable implementation behavior from firmware commit `97c2b6ba195a830836164daaa9da260c8eee8dde`. Relevant Git history and authorship are retained with paths filtered to the core. Extraction changes repository/build ownership, not the existing firmware's persistent format or product version.
