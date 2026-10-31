/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.text.ttml;

import android.text.Spanned;

/**
 * A span used to mark a section of text for later deletion.
 *
 * <p>This is deliberately package-private because it's not generally supported by Android and
 * results in surprising behaviour when simply calling {@link Spanned#toString} (i.e. the text isn't
 * deleted).
 *
 * <p>This span is explicitly handled in {@code TtmlNode#cleanUpText}.
 */
/* package */ final class DeleteTextSpan {}
