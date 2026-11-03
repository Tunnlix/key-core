#ifndef CTAPHID_HANDLERS_H
#define CTAPHID_HANDLERS_H

#include "protocol/ctaphid_reassembler.h"
#include "protocol/ctaphid_response.h"

/* Inputs are borrowed, immutable, and validated by the dispatcher.
 * INIT constructs its reply using the CID selected by the dispatcher; it does
 * not allocate channels or reset transaction state. PING echoes the payload.
 * WINK sends an empty reply after the caller's platform identification action.
 * These handlers return serialization/transport status without modifying the
 * request. CBOR execution and cancellation belong to the device/backend;
 * stateful LOCK ownership belongs to ctaphid_device, outside these handlers.
 */
/* Product version is supplied by the integration. NULL means 0.0.0. */
CtaphidResponseResult ctaphid_handle_init_with_version(
    const CtaphidReassembler *message, uint32_t allocated_channel_id,
    uint8_t capabilities, const uint8_t device_version[3],
    CtaphidSendReport send_report, void *transport_context);
/* Convenience variant with an unspecified (0.0.0) product version. */
CtaphidResponseResult ctaphid_handle_init(
    const CtaphidReassembler *message,
    uint32_t allocated_channel_id,
    uint8_t capabilities,
    CtaphidSendReport send_report,
    void *transport_context
);
CtaphidResponseResult ctaphid_handle_ping(
    const CtaphidReassembler *message,
    CtaphidSendReport send_report,
    void *transport_context
);
CtaphidResponseResult ctaphid_handle_wink(
    const CtaphidReassembler *message,
    CtaphidSendReport send_report,
    void *transport_context
);

#endif
