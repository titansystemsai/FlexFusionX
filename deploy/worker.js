// Serves the static site; sends www.flexfusionx.com.au to the bare domain.
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.hostname === "www.flexfusionx.com.au") {
      url.hostname = "flexfusionx.com.au";
      return Response.redirect(url.toString(), 301);
    }
    return env.ASSETS.fetch(request);
  },
};
