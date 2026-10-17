// Serves the static site. Forces HTTPS and sends www.flexfusionx.com.au to the bare domain.
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.protocol === "http:" || url.hostname === "www.flexfusionx.com.au") {
      url.protocol = "https:";
      url.hostname = "flexfusionx.com.au";
      return Response.redirect(url.toString(), 301);
    }
    return env.ASSETS.fetch(request);
  },
};
