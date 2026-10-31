/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.source.hls.playlist;

import androidx.annotation.Nullable;
import com.google.android.exoplayer2.upstream.ParsingLoadable;

/** Factory for {@link HlsPlaylist} parsers. */
public interface HlsPlaylistParserFactory {

  /**
   * Returns a stand-alone playlist parser. Playlists parsed by the returned parser do not inherit
   * any attributes from other playlists.
   */
  ParsingLoadable.Parser<HlsPlaylist> createPlaylistParser();

  /**
   * Returns a playlist parser for playlists that were referenced by the given {@link
   * HlsMultivariantPlaylist}. Returned {@link HlsMediaPlaylist} instances may inherit attributes
   * from {@code multivariantPlaylist}.
   *
   * @param multivariantPlaylist The multivariant playlist that referenced any parsed media
   *     playlists.
   * @param previousMediaPlaylist The previous media playlist or null if there is no previous media
   *     playlist.
   * @return A parser for HLS playlists.
   */
  ParsingLoadable.Parser<HlsPlaylist> createPlaylistParser(
      HlsMultivariantPlaylist multivariantPlaylist,
      @Nullable HlsMediaPlaylist previousMediaPlaylist);
}
