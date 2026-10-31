/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.mediacodec;

import android.media.MediaCodec;
import com.google.android.exoplayer2.mediacodec.MediaCodecUtil.DecoderQueryException;
import java.util.List;

/** Selector of {@link MediaCodec} instances. */
public interface MediaCodecSelector {

  /**
   * Default implementation of {@link MediaCodecSelector}, which returns the preferred decoder for
   * the given format.
   */
  MediaCodecSelector DEFAULT = MediaCodecUtil::getDecoderInfos;

  /**
   * Returns a list of decoders that can decode media in the specified MIME type, in priority order.
   *
   * @param mimeType The MIME type for which a decoder is required.
   * @param requiresSecureDecoder Whether a secure decoder is required.
   * @param requiresTunnelingDecoder Whether a tunneling decoder is required.
   * @return An unmodifiable list of {@link MediaCodecInfo}s corresponding to decoders. May be
   *     empty.
   * @throws DecoderQueryException Thrown if there was an error querying decoders.
   */
  List<MediaCodecInfo> getDecoderInfos(
      String mimeType, boolean requiresSecureDecoder, boolean requiresTunnelingDecoder)
      throws DecoderQueryException;
}
