/*
 * Copyright (C) Nikolai Kudashov
 *
 * Licensed under GNU GPLv3.
 */

package org.telegram.tgnet;

public interface ResultCallback<T> {

    void onComplete(T result);

    default void onError(TLRPC.TL_error error) {}

    default void onError(Throwable throwable) {}
}
