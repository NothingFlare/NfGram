/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.offline;

/** Creates {@link Downloader Downloaders} for given {@link DownloadRequest DownloadRequests}. */
public interface DownloaderFactory {

  /**
   * Creates a {@link Downloader} to perform the given {@link DownloadRequest}.
   *
   * @param request The download request.
   * @return The downloader.
   */
  Downloader createDownloader(DownloadRequest request);
}
