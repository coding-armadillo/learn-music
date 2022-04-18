<script>
  document.addEventListener('DOMContentLoaded', () => {
    (document.querySelectorAll('.delete') || []).forEach(($delete) => {
      $notification = $delete.parentNode;
      setTimeout(function(){
        if($notification.parentNode) {
          $notification.parentNode.removeChild($notification)
        }
      }, 5000);
      $delete.addEventListener('click', () => {
        $notification.parentNode.removeChild($notification);
      });
    });
  });
</script>
