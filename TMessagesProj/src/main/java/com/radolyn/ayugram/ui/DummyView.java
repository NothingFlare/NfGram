/*
 * Copyright (C) Radolyn
 *
 * Licensed under GNU GPLv3.
 */

package com.radolyn.ayugram.ui;

import android.annotation.SuppressLint;
import android.content.Context;
import android.view.View;
import org.telegram.messenger.MessageObject;

@SuppressLint("ViewConstructor")
public class DummyView extends View {
    private MessageObject messageObject;

    public DummyView(Context context) {
        super(context);

        // hacky way to make view visible
        // for `chatLayoutManager.findFirstVisibleItemPosition()`
        // ...and yes, it eats 1px, so what?
        setMinimumHeight(1);
    }

    public MessageObject getMessageObject() {
        return messageObject;
    }

    public void setMessageObject(MessageObject messageObject) {
        this.messageObject = messageObject;
    }
}
