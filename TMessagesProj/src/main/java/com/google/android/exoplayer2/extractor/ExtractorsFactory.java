/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.extractor;

import android.net.Uri;
import java.util.List;
import java.util.Map;

/** Factory for arrays of {@link Extractor} instances. */
public interface ExtractorsFactory {

  /**
   * Extractor factory that returns an empty list of extractors. Can be used whenever {@link
   * Extractor Extractors} are not required.
   */
  ExtractorsFactory EMPTY = () -> new Extractor[] {};

  /** Returns an array of new {@link Extractor} instances. */
  Extractor[] createExtractors();

  /**
   * Returns an array of new {@link Extractor} instances.
   *
   * @param uri The {@link Uri} of the media to extract.
   * @param responseHeaders The response headers of the media to extract, or an empty map if there
   *     are none. The map lookup should be case-insensitive.
   * @return The {@link Extractor} instances.
   */
  default Extractor[] createExtractors(Uri uri, Map<String, List<String>> responseHeaders) {
    return createExtractors();
  }
}
