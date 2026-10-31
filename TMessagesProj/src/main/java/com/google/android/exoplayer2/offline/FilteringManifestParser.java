/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.offline;

import android.net.Uri;
import androidx.annotation.Nullable;
import com.google.android.exoplayer2.upstream.ParsingLoadable.Parser;
import java.io.IOException;
import java.io.InputStream;
import java.util.List;

/**
 * A manifest parser that includes only the streams identified by the given stream keys.
 *
 * @param <T> The {@link FilterableManifest} type.
 */
public final class FilteringManifestParser<T extends FilterableManifest<T>> implements Parser<T> {

  private final Parser<? extends T> parser;
  @Nullable private final List<StreamKey> streamKeys;

  /**
   * @param parser A parser for the manifest that will be filtered.
   * @param streamKeys The stream keys. If null or empty then filtering will not occur.
   */
  public FilteringManifestParser(Parser<? extends T> parser, @Nullable List<StreamKey> streamKeys) {
    this.parser = parser;
    this.streamKeys = streamKeys;
  }

  @Override
  public T parse(Uri uri, InputStream inputStream) throws IOException {
    T manifest = parser.parse(uri, inputStream);
    return streamKeys == null || streamKeys.isEmpty() ? manifest : manifest.copy(streamKeys);
  }
}
