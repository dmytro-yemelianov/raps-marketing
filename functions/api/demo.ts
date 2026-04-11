interface Env {
  // Add KV_NAMESPACE or D1_DATABASE bindings here when ready
}

export const onRequestPost: PagesFunction<Env> = async (context) => {
  const body = await context.request.json();
  console.log('Demo request:', JSON.stringify(body));
  return new Response(JSON.stringify({ ok: true }), {
    headers: { 'Content-Type': 'application/json' },
  });
};
