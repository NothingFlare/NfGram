/*
 * Copyright (C) Nikolai Kudashov
 *
 * Licensed under GNU GPLv3.
 */

package org.telegram.ui.Components.FloatingDebug;

import java.util.List;

public interface FloatingDebugProvider {
    List<FloatingDebugController.DebugItem> onGetDebugItems();
}
