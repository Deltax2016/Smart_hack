package com.google.appinventor.components.runtime.util;

import android.util.Log;
import java.util.ArrayList;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class RetValManager {
    private static final String LOG_TAG = "RetValManager";
    private static final long TENSECONDS = 10000;
    private static ArrayList<JSONObject> currentArray = new ArrayList(10);
    private static final Object semaphore = new Object();

    private RetValManager() {
    }

    public static void appendReturnValue(String blockid, String ok, String item) {
        synchronized (semaphore) {
            JSONObject retval = new JSONObject();
            try {
                retval.put("status", (Object) ok);
                retval.put("type", (Object) "return");
                retval.put("value", (Object) item);
                retval.put("blockid", (Object) blockid);
                boolean sendNotify = currentArray.isEmpty();
                currentArray.add(retval);
                if (sendNotify) {
                    semaphore.notifyAll();
                }
            } catch (JSONException e) {
                Log.e(LOG_TAG, "Error building retval", e);
            }
        }
    }

    public static void sendError(String error) {
        synchronized (semaphore) {
            JSONObject retval = new JSONObject();
            try {
                retval.put("status", (Object) "OK");
                retval.put("type", (Object) "error");
                retval.put("value", (Object) error);
                boolean sendNotify = currentArray.isEmpty();
                currentArray.add(retval);
                if (sendNotify) {
                    semaphore.notifyAll();
                }
            } catch (JSONException e) {
                Log.e(LOG_TAG, "Error building retval", e);
            }
        }
    }

    public static void pushScreen(String screenName, Object value) {
        synchronized (semaphore) {
            JSONObject retval = new JSONObject();
            try {
                retval.put("status", (Object) "OK");
                retval.put("type", (Object) "pushScreen");
                retval.put("screen", (Object) screenName);
                if (value != null) {
                    retval.put("value", value.toString());
                }
                boolean sendNotify = currentArray.isEmpty();
                currentArray.add(retval);
                if (sendNotify) {
                    semaphore.notifyAll();
                }
            } catch (JSONException e) {
                Log.e(LOG_TAG, "Error building retval", e);
            }
        }
    }

    public static void popScreen(String value) {
        synchronized (semaphore) {
            JSONObject retval = new JSONObject();
            try {
                retval.put("status", (Object) "OK");
                retval.put("type", (Object) "popScreen");
                if (value != null) {
                    retval.put("value", value.toString());
                }
                boolean sendNotify = currentArray.isEmpty();
                currentArray.add(retval);
                if (sendNotify) {
                    semaphore.notifyAll();
                }
            } catch (JSONException e) {
                Log.e(LOG_TAG, "Error building retval", e);
            }
        }
    }

    public static String fetch(boolean block) {
        String jSONObject;
        long startTime = System.currentTimeMillis();
        synchronized (semaphore) {
            while (currentArray.isEmpty() && block && System.currentTimeMillis() - startTime <= 9900) {
                try {
                    semaphore.wait(TENSECONDS);
                } catch (InterruptedException e) {
                }
            }
            Object arrayoutput = new JSONArray(currentArray);
            JSONObject output = new JSONObject();
            try {
                output.put("status", (Object) "OK");
                output.put("values", arrayoutput);
                currentArray.clear();
                jSONObject = output.toString();
            } catch (JSONException e2) {
                Log.e(LOG_TAG, "Error fetching retvals", e2);
                jSONObject = "{\"status\" : \"BAD\", \"message\" : \"Failure in RetValManager\"}";
            }
        }
        return jSONObject;
    }
}
