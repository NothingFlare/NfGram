/*
 * Copyright (C) Nikolai Kudashov
 *
 * Licensed under GNU GPLv3.
 */

package org.telegram.messenger;

import org.telegram.tgnet.TLObject;

public class DownloadObject {
    public TLObject object;
    public int type;
    public long id;
    public boolean secret;
    public boolean forceCache;
    public String parent;
}
