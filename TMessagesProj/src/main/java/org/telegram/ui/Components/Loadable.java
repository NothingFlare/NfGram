/*
 * Copyright (C) Nikolai Kudashov
 *
 * Licensed under GNU GPLv3.
 */

package org.telegram.ui.Components;

public interface Loadable {
    void setLoading(boolean loading);
    boolean isLoading();
}
