/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.source.hls;

import com.google.android.exoplayer2.source.hls.playlist.HlsMasterPlaylist;
import com.google.android.exoplayer2.source.hls.playlist.HlsMediaPlaylist;
import com.google.android.exoplayer2.source.hls.playlist.HlsMultivariantPlaylist;

/** Holds a multivariant playlist along with a snapshot of one of its media playlists. */
public final class HlsManifest {

  /**
   * @deprecated Use {@link #multivariantPlaylist} instead.
   */
  @Deprecated
  @SuppressWarnings("deprecation") // Keeping deprecated field with deprecated class.
  public final HlsMasterPlaylist masterPlaylist;
  /** The multivariant playlist of an HLS stream. */
  public final HlsMultivariantPlaylist multivariantPlaylist;
  /** A snapshot of a media playlist referred to by {@link #multivariantPlaylist}. */
  public final HlsMediaPlaylist mediaPlaylist;

  /**
   * @param multivariantPlaylist The multivariant playlist.
   * @param mediaPlaylist The media playlist.
   */
  @SuppressWarnings("deprecation") // Intentionally creating deprecated hlsMasterPlaylist field.
  /* package */ HlsManifest(
      HlsMultivariantPlaylist multivariantPlaylist, HlsMediaPlaylist mediaPlaylist) {
    this.multivariantPlaylist = multivariantPlaylist;
    this.mediaPlaylist = mediaPlaylist;
    this.masterPlaylist =
        new HlsMasterPlaylist(
            multivariantPlaylist.baseUri,
            multivariantPlaylist.tags,
            multivariantPlaylist.variants,
            multivariantPlaylist.videos,
            multivariantPlaylist.audios,
            multivariantPlaylist.subtitles,
            multivariantPlaylist.closedCaptions,
            multivariantPlaylist.muxedAudioFormat,
            multivariantPlaylist.muxedCaptionFormats,
            multivariantPlaylist.hasIndependentSegments,
            multivariantPlaylist.variableDefinitions,
            multivariantPlaylist.sessionKeyDrmInitData);
  }
}
