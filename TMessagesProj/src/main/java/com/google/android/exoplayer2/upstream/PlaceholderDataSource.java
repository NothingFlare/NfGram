/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.upstream;

import android.net.Uri;
import androidx.annotation.Nullable;
import java.io.IOException;

/** A DataSource which provides no data. {@link #open(DataSpec)} throws {@link IOException}. */
public final class PlaceholderDataSource implements DataSource {

  public static final PlaceholderDataSource INSTANCE = new PlaceholderDataSource();

  /** A factory that produces {@link PlaceholderDataSource}. */
  public static final Factory FACTORY = PlaceholderDataSource::new;

  private PlaceholderDataSource() {}

  @Override
  public void addTransferListener(TransferListener transferListener) {
    // Do nothing.
  }

  @Override
  public long open(DataSpec dataSpec) throws IOException {
    throw new IOException("PlaceholderDataSource cannot be opened");
  }

  @Override
  public int read(byte[] buffer, int offset, int length) {
    throw new UnsupportedOperationException();
  }

  @Override
  @Nullable
  public Uri getUri() {
    return null;
  }

  @Override
  public void close() {
    // do nothing.
  }
}
