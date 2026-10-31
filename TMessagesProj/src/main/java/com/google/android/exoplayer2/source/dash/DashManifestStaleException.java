/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.source.dash;

import java.io.IOException;

/** Thrown when a live playback's manifest is stale and a new manifest could not be loaded. */
public final class DashManifestStaleException extends IOException {}
