/*
 * Copyright (C) Nikolai Kudashov
 *
 * Licensed under GNU GPLv3.
 */

package org.telegram.tgnet;

public interface RequestDelegateTimestamp {
    void run(TLObject response, TLRPC.TL_error error, long responseTime);
}
