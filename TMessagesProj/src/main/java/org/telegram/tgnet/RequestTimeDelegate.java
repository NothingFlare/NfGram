/*
 * Copyright (C) Nikolai Kudashov
 *
 * Licensed under GNU GPLv3.
 */

package org.telegram.tgnet;

public interface RequestTimeDelegate {
    void run(long time);
}
