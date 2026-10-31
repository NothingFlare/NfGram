/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.util;

import android.view.SurfaceView;
import androidx.annotation.Nullable;

/** Provider for views to show diagnostic information during a transformation, for debugging. */
public interface DebugViewProvider {

  /** Debug view provider that doesn't show any debug info. */
  DebugViewProvider NONE = (int width, int height) -> null;

  /**
   * Returns a new surface view to show a preview of transformer output with the given width/height
   * in pixels, or {@code null} if no debug information should be shown.
   *
   * <p>This method may be called on an arbitrary thread.
   */
  @Nullable
  SurfaceView getDebugPreviewSurfaceView(int width, int height);
}
