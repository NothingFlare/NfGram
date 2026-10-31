/*
 * Copyright (C) Nikolai Kudashov
 *
 * Licensed under GNU GPLv3.
 */

package com.android.internal.telephony;

public interface ITelephony {
    boolean endCall();

    void answerRingingCall();

    void silenceRinger();
}
