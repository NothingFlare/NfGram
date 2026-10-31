/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.offline;

import java.util.List;

/**
 * A manifest that can generate copies of itself including only the streams specified by the given
 * keys.
 *
 * @param <T> The manifest type.
 */
public interface FilterableManifest<T> {

  /**
   * Returns a copy of the manifest including only the streams specified by the given keys. If the
   * manifest is unchanged then the instance may return itself.
   *
   * @param streamKeys A non-empty list of stream keys.
   * @return The filtered manifest.
   */
  T copy(List<StreamKey> streamKeys);
}
