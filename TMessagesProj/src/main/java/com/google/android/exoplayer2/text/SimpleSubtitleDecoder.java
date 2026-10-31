/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.text;

import androidx.annotation.Nullable;
import com.google.android.exoplayer2.C;
import com.google.android.exoplayer2.decoder.SimpleDecoder;
import com.google.android.exoplayer2.util.Assertions;
import java.nio.ByteBuffer;

/** Base class for subtitle parsers that use their own decode thread. */
public abstract class SimpleSubtitleDecoder
    extends SimpleDecoder<SubtitleInputBuffer, SubtitleOutputBuffer, SubtitleDecoderException>
    implements SubtitleDecoder {

  private final String name;

  /**
   * @param name The name of the decoder.
   */
  @SuppressWarnings("nullness:method.invocation")
  protected SimpleSubtitleDecoder(String name) {
    super(new SubtitleInputBuffer[2], new SubtitleOutputBuffer[2]);
    this.name = name;
    setInitialInputBufferSize(1024);
  }

  @Override
  public final String getName() {
    return name;
  }

  @Override
  public void setPositionUs(long positionUs) {
    // Do nothing
  }

  @Override
  protected final SubtitleInputBuffer createInputBuffer() {
    return new SubtitleInputBuffer();
  }

  @Override
  protected final SubtitleOutputBuffer createOutputBuffer() {
    return new SubtitleOutputBuffer() {
      @Override
      public void release() {
        SimpleSubtitleDecoder.this.releaseOutputBuffer(this);
      }
    };
  }

  @Override
  protected final SubtitleDecoderException createUnexpectedDecodeException(Throwable error) {
    return new SubtitleDecoderException("Unexpected decode error", error);
  }

  @SuppressWarnings("ByteBufferBackingArray")
  @Override
  @Nullable
  protected final SubtitleDecoderException decode(
      SubtitleInputBuffer inputBuffer, SubtitleOutputBuffer outputBuffer, boolean reset) {
    try {
      ByteBuffer inputData = Assertions.checkNotNull(inputBuffer.data);
      Subtitle subtitle = decode(inputData.array(), inputData.limit(), reset);
      outputBuffer.setContent(inputBuffer.timeUs, subtitle, inputBuffer.subsampleOffsetUs);
      // Clear BUFFER_FLAG_DECODE_ONLY (see [Internal: b/27893809]).
      outputBuffer.clearFlag(C.BUFFER_FLAG_DECODE_ONLY);
      return null;
    } catch (SubtitleDecoderException e) {
      return e;
    }
  }

  /**
   * Decodes data into a {@link Subtitle}.
   *
   * @param data An array holding the data to be decoded, starting at position 0.
   * @param length The number of bytes from {@code data} to be decoded.
   * @param reset Whether the decoder must be reset before decoding.
   * @return The decoded {@link Subtitle}.
   * @throws SubtitleDecoderException If a decoding error occurs.
   */
  protected abstract Subtitle decode(byte[] data, int length, boolean reset)
      throws SubtitleDecoderException;
}
