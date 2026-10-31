/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.source.hls.playlist;

import androidx.annotation.Nullable;
import com.google.android.exoplayer2.Format;
import com.google.android.exoplayer2.drm.DrmInitData;
import java.util.List;
import java.util.Map;

/**
 * @deprecated Use {@link HlsMultivariantPlaylist} instead.
 */
@Deprecated
public final class HlsMasterPlaylist extends HlsMultivariantPlaylist {

  /**
   * Creates an HLS multivariant playlist.
   *
   * @deprecated Use {@link HlsMultivariantPlaylist#HlsMultivariantPlaylist} instead.
   */
  @Deprecated
  public HlsMasterPlaylist(
      String baseUri,
      List<String> tags,
      List<Variant> variants,
      List<Rendition> videos,
      List<Rendition> audios,
      List<Rendition> subtitles,
      List<Rendition> closedCaptions,
      @Nullable Format muxedAudioFormat,
      @Nullable List<Format> muxedCaptionFormats,
      boolean hasIndependentSegments,
      Map<String, String> variableDefinitions,
      List<DrmInitData> sessionKeyDrmInitData) {
    super(
        baseUri,
        tags,
        variants,
        videos,
        audios,
        subtitles,
        closedCaptions,
        muxedAudioFormat,
        muxedCaptionFormats,
        hasIndependentSegments,
        variableDefinitions,
        sessionKeyDrmInitData);
  }
}
