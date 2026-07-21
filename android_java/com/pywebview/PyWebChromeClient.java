package com.pywebview;

import android.webkit.WebChromeClient;
import android.webkit.WebView;
import android.webkit.PermissionRequest;

public class PyWebChromeClient extends WebChromeClient {
    private EventCallbackWrapper callbackWrapper;

    public void setCallback(EventCallbackWrapper callbackWrapper) {
        this.callbackWrapper = callbackWrapper;
    }

    @Override
    public void onPermissionRequest(final PermissionRequest request) {
        request.grant(request.getResources());
    }
}
