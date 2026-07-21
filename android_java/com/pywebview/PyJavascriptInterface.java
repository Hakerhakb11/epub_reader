package com.pywebview;

import android.webkit.JavascriptInterface;

public class PyJavascriptInterface {
    private JsApiCallbackWrapper callbackWrapper;

    public void setCallback(JsApiCallbackWrapper callbackWrapper) {
        this.callbackWrapper = callbackWrapper;
    }

    @JavascriptInterface
    public String call(String method, String params, String id) {
        if (callbackWrapper != null) {
            return callbackWrapper.call(method, params, id);
        }
        return "";
    }
}
