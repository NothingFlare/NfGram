/*
 * Copyright (C) Nikolai Kudashov
 *
 * Licensed under GNU GPLv3.
 */

package org.telegram.messenger;

public interface GenericProvider<F, T> {
    T provide(F obj);
}
