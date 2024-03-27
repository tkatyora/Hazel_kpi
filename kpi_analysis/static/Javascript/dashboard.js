// $(document).ready(function() {
//     var no_quotations = "{{ cache.get('no_quotations') }}";
//     if (no_quotations == 'true') {
//         // Display your message here
//         $("#message").show();
//         // Set a timeout to hide the message after 1 hour
//         setTimeout(function() {
//             $("#message").hide();
//         }, 60*60*1000);  // 1 hour in milliseconds
//     }
// });
// from django.core.cache import cache

// def check_quotations(request):
//     # Check if there are any pending quotations
//     quotations = Quotation.objects.filter(status='pending')
//     if not quotations:
//         # If no pending quotations, set a cache key
//         cache.set('no_quotations', 'true', 60*60)  # Cache for 1 hour