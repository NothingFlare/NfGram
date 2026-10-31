/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.video;

import android.graphics.SurfaceTexture;

/** A listener for metadata corresponding to video being rendered. */
public interface VideoListener {

  default void onSurfaceSizeChanged(int width, int height) {}

  boolean onSurfaceDestroyed(SurfaceTexture surfaceTexture);
  void onSurfaceTextureUpdated(SurfaceTexture surfaceTexture);
}
