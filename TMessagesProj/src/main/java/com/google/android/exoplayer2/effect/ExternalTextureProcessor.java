/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.effect;

/**
 * Interface for a {@link GlTextureProcessor} that samples from an external texture.
 *
 * <p>Use {@link #setTextureTransformMatrix(float[])} to provide the texture's transformation
 * matrix.
 */
/* package */ interface ExternalTextureProcessor extends GlTextureProcessor {

  /**
   * Sets the texture transform matrix for converting an external surface texture's coordinates to
   * sampling locations.
   *
   * @param textureTransformMatrix The external surface texture's {@linkplain
   *     android.graphics.SurfaceTexture#getTransformMatrix(float[]) transform matrix}.
   */
  void setTextureTransformMatrix(float[] textureTransformMatrix);
}
