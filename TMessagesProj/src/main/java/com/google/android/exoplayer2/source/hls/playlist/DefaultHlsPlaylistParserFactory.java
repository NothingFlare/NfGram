/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.source.hls.playlist;

import androidx.annotation.Nullable;
import com.google.android.exoplayer2.upstream.ParsingLoadable;

/** Default implementation for {@link HlsPlaylistParserFactory}. */
public final class DefaultHlsPlaylistParserFactory implements HlsPlaylistParserFactory {

  @Override
  public ParsingLoadable.Parser<HlsPlaylist> createPlaylistParser() {
    return new HlsPlaylistParser();
  }

  @Override
  public ParsingLoadable.Parser<HlsPlaylist> createPlaylistParser(
      HlsMultivariantPlaylist multivariantPlaylist,
      @Nullable HlsMediaPlaylist previousMediaPlaylist) {
    return new HlsPlaylistParser(multivariantPlaylist, previousMediaPlaylist);
  }
}
