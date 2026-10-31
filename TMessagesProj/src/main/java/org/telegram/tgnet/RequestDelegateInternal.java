/*
 * Copyright (C) Nikolai Kudashov
 *
 * Licensed under GNU GPLv3.
 */

package org.telegram.tgnet;

public interface RequestDelegateInternal {
    void run(long response, int errorCode, String errorText, int networkType, long timestamp, long requestMsgId, int dcId);
}
