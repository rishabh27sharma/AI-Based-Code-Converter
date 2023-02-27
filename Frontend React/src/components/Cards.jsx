import Card from 'react-bootstrap/Card';
import Upload from "../images/upload.png";
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
// import $ from 'jquery';

export const Cards = () => {

  const handleFile = () => {
   var thefile = document.getElementById('fileInput');
   if(thefile.files.length === 0 ){
    alert("File not selected!\nPlease select a file.");
  } else{
    toast("Please wait... Generated Output File is downloading!");
  }
  }

  return (
    <>
    <Card style={{ width: '19rem' }} className="card-container">
      <Card.Img variant="top" src={Upload} alt="upload" />
      <Card.Body>
        <Card.Title>Upload Your File Here</Card.Title>
        <form action='http://localhost:5000/uploader' method = "POST" enctype = "multipart/form-data">
         <input className='insert'  type = "file" name = "file" id='fileInput'/>
         <button className='btn-upload' type="submit" onClick={handleFile}><i class="fa-solid fa-upload"></i> Upload</button>
         <button className='btn-reset' type='reset'><i class="fa-solid fa-rotate-left"></i> Reset</button>
         <ToastContainer autoClose={18000} />
        </form>
      </Card.Body>
    </Card>
    </>
  )
}
