/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.upstream;

import android.net.Uri;
import androidx.annotation.Nullable;
import com.google.android.exoplayer2.C;
import com.google.android.exoplayer2.util.Assertions;
import java.io.IOException;
import java.util.Collections;
import java.util.List;
import java.util.Map;

/**
 * {@link DataSource} wrapper which keeps track of bytes transferred, redirected uris, and response
 * headers.
 */
public final class StatsDataSource implements DataSource {

  private final DataSource dataSource;

  private long bytesRead;
  private Uri lastOpenedUri;
  private Map<String, List<String>> lastResponseHeaders;

  /**
   * Creates the stats data source.
   *
   * @param dataSource The wrapped {@link DataSource}.
   */
  public StatsDataSource(DataSource dataSource) {
    this.dataSource = Assertions.checkNotNull(dataSource);
    lastOpenedUri = Uri.EMPTY;
    lastResponseHeaders = Collections.emptyMap();
  }

  /** Resets the number of bytes read as returned from {@link #getBytesRead()} to zero. */
  public void resetBytesRead() {
    bytesRead = 0;
  }

  /** Returns the total number of bytes that have been read from the data source. */
  public long getBytesRead() {
    return bytesRead;
  }

  /**
   * Returns the {@link Uri} associated with the last {@link #open(DataSpec)} call. If redirection
   * occurred, this is the redirected uri.
   */
  public Uri getLastOpenedUri() {
    return lastOpenedUri;
  }

  /** Returns the response headers associated with the last {@link #open(DataSpec)} call. */
  public Map<String, List<String>> getLastResponseHeaders() {
    return lastResponseHeaders;
  }

  @Override
  public void addTransferListener(TransferListener transferListener) {
    Assertions.checkNotNull(transferListener);
    dataSource.addTransferListener(transferListener);
  }

  @Override
  public long open(DataSpec dataSpec) throws IOException {
    // Reassign defaults in case dataSource.open throws an exception.
    lastOpenedUri = dataSpec.uri;
    lastResponseHeaders = Collections.emptyMap();
    long availableBytes = dataSource.open(dataSpec);
    lastOpenedUri = Assertions.checkNotNull(getUri());
    lastResponseHeaders = getResponseHeaders();
    return availableBytes;
  }

  @Override
  public int read(byte[] buffer, int offset, int length) throws IOException {
    int bytesRead = dataSource.read(buffer, offset, length);
    if (bytesRead != C.RESULT_END_OF_INPUT) {
      this.bytesRead += bytesRead;
    }
    return bytesRead;
  }

  @Override
  @Nullable
  public Uri getUri() {
    return dataSource.getUri();
  }

  @Override
  public Map<String, List<String>> getResponseHeaders() {
    return dataSource.getResponseHeaders();
  }

  @Override
  public void close() throws IOException {
    dataSource.close();
  }
}
