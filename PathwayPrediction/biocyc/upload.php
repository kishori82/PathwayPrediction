<?php
  if (is_uploaded_file($_FILES['myfile']['tmp_name']) && $_FILES['my-file']['error']==0) {
    echo "The file was uploaded successfully but has not been saved.<br>";
    echo "The file is temporarily stored: " . $_FILES['my-file']['tmp_name'] . "<br>";
    echo "The file name was: " . $_FILES['my-file']['name'] . "<br>";
    echo "The file type is: " . $_FILES['my-file']['type'] . "<br>";
    echo "The file size is: " . $_FILES['my-file']['size'] . "<br>";
  } else {
    echo "The file was not uploaded successfully.";
    echo "(Error Code:" . $_FILES['my-file']['error'] . ")";
  }
?>
