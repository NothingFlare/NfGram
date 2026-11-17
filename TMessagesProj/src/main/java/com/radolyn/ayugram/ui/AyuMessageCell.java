/*
 * Copyright (C) Radolyn
 *
 * Licensed under GNU GPLv3.
 */

package com.radolyn.ayugram.ui;

import android.app.Activity;
import android.content.Context;
import android.text.TextUtils;
import com.radolyn.ayugram.database.entities.EditedMessage;
import org.telegram.messenger.AndroidUtilities;
import org.telegram.messenger.LocaleController;
import org.telegram.messenger.R;
import org.telegram.ui.ActionBar.BaseFragment;
import org.telegram.ui.Cells.ChatMessageCell;
import org.telegram.ui.Components.BulletinFactory;

public class AyuMessageCell extends ChatMessageCell {
    private EditedMessage editedMessage;
    private String currentThumbPath;

    public AyuMessageCell(Context context, Activity activity, BaseFragment fragment) {
        super(context, fragment != null ? fragment.getCurrentAccount() : org.telegram.messenger.UserConfig.selectedAccount);

        setFullyDraw(true);
        isChat = false;
        setDelegate(new ChatMessageCell.ChatMessageCellDelegate() {
        });

        setOnClickListener(v -> {
            if (editedMessage == null) {
                return;
            }
            // copy only if no media
            if (TextUtils.isEmpty(editedMessage.mediaPath)) {
                copyText(fragment);
            }

            // ..open media otherwise
            if (!TextUtils.isEmpty(editedMessage.mediaPath) && activity != null && !activity.isFinishing() && getMessageObject() != null) {
                AndroidUtilities.openForView(getMessageObject(), activity, null, false);
            }
        });

        setOnLongClickListener(v -> {
            if (editedMessage != null) {
                copyText(fragment);
            }
            return true;
        });
    }

    public void setEditedMessage(EditedMessage editedMessage) {
        this.editedMessage = editedMessage;
        updateThumbnail();
    }

    private void updateThumbnail() {
        if (editedMessage != null && !TextUtils.isEmpty(editedMessage.hqThumbPath)) {
            if (!TextUtils.equals(currentThumbPath, editedMessage.hqThumbPath)) {
                currentThumbPath = editedMessage.hqThumbPath;
                if (getPhotoImage() != null) {
                    getPhotoImage().setImage(editedMessage.hqThumbPath, null, null, null, 0);
                }
            }
        } else {
            currentThumbPath = null;
        }
    }

    private void copyText(BaseFragment fragment) {
        if (editedMessage != null && !TextUtils.isEmpty(editedMessage.text)) {
            AndroidUtilities.addToClipboard(editedMessage.text);
            if (fragment != null && fragment.getParentActivity() != null && !fragment.getParentActivity().isFinishing()) {
                try {
                    BulletinFactory.of(fragment).createCopyBulletin(LocaleController.getString("MessageCopied", R.string.MessageCopied)).show();
                } catch (Throwable ignored) {}
            }
        }
    }

    @Override
    protected void onLayout(boolean changed, int left, int top, int right, int bottom) {
        super.onLayout(changed, left, top, right, bottom);
        if (changed) {
            updateThumbnail();
        }
    }
}
