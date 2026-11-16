/* Template for plugging an existing widget into a band.
 * A panel module default-exports mount(host, ctx) and may return a cleanup function.
 * ctx = { state, registry, manifest, d3, getJson, bundleUrl, doc }
 * ctx.state is the shared state: read ctx.state.get(), react with ctx.state.subscribe(fn), change with ctx.state.set({...}).
 * Build DOM with textContent / createElement (never innerHTML with values from data or the URL).
 */
export default function mount(host, ctx) {
  const pre = ctx.doc.createElement("pre");
  host.append(pre);
  const draw = (s) => { pre.textContent = JSON.stringify(s, null, 1); };
  draw(ctx.state.get());
  return ctx.state.subscribe(draw);   // subscribe returns the cleanup function
}
