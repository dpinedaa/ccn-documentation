const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const cors = require('cors');




const { Schema } = mongoose;

// Define a schema for documents
const documentSchema = new Schema({
  _id: {type: String, alias: 'customer_document'},
  name: String,
  portVue: Number,
  portFlask: Number,
  portApache: Number,
  customerName: String
});




// Define a schema for customers
const customerSchema = new Schema({
  name: String,
  documents: [documentSchema],
});

// Create models from the schemas
const Document = mongoose.model('Document', documentSchema);
const Customer = mongoose.model('Customer', customerSchema);

const app = express();
const port = process.env.PORT || 3000;

app.use(bodyParser.json());

app.use(cors());

// Connect to MongoDB
mongoose.connect('mongodb://192.168.6.79:27017/customers', { useNewUrlParser: true, useUnifiedTopology: true });
const db = mongoose.connection;

db.on('error', console.error.bind(console, 'MongoDB connection error:'));
db.once('open', () => {
  console.log('Connected to MongoDB');
});

//Add a customer 

app.post('/add-customer', async (req, res) => {
    try {
      const { name, documents } = req.body;
  
      // Create a new customer
      const customer = new Customer({
        name,
        documents: documents || [], // If documents are not provided, set to an empty array
      });
  
      // Save the customer to the database
      await customer.save();
  
      res.status(201).json(customer);
    } catch (error) {
      console.error(error);
      res.status(500).json({ error: 'Internal Server Error' });
    }
  });
  

// Get all customers
app.get('/customers', async (req, res) => {
try {
    const customers = await Customer.find();
    res.status(200).json(customers);
} catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal Server Error' });
}
});

//Delete a customer
app.delete('/customers/:id', async (req, res) => {
    try {
      const { id } = req.params;
  
      // Delete the customer
      await Customer.findByIdAndDelete(id);
  
      res.status(200).json({ message: 'Customer deleted successfully' });
    } catch (error) {
      console.error(error);
      res.status(500).json({ error: 'Internal Server Error' });
    }
  });

  // Delete all customers 
app.delete('/customers', async (req, res) => {
    try {
      // Delete all customers
      await Customer.deleteMany();
  
      res.status(200).json({ message: 'Customers deleted successfully' });
    } catch (error) {
      console.error(error);
      res.status(500).json({ error: 'Internal Server Error' });
    }
});













// Add a document to a customer
app.post('/add-document/:customerId', async (req, res) => {
    try {
    
      const customerId = req.params.customerId;
      const { name } = req.body;

      //Find the customer by ID 
      const foundCustomer = await Customer.findById(customerId);
      const customerName = foundCustomer.name;

      
      // Generate and assign ports based on specified ranges
      const portVue = await generateUniquePort(2003, 4000);
      const portFlask = await generateUniquePort(4003, 6000);
      const portApache = await generateUniquePort(6003, 8000);
      const customer_document = customerName + "-" + name;
      // Create a new document
      const document = new Document({
        customer_document,
        name,
        portVue,
        portFlask,
        portApache,
      });
  
      // Find the customer by ID
      const customer = await Customer.findById(customerId);
  
      if (!customer) {
        return res.status(404).json({ error: 'Customer not found' });
      }
  
      // Check for port duplications within all the existing documents
      const isPortDuplicated = customer.documents.some(doc => (
        doc.portVue === portVue || doc.portFlask === portFlask || doc.portApache === portApache
      ));
  
      if (isPortDuplicated) {
        return res.status(400).json({ error: 'Port duplication detected' });
      }
  
      // Add the document to the customer
      customer.documents.push(document);
  
      // Save the updated customer to the database
      await customer.save();
  
      res.status(201).json(document);
    } catch (error) {
      console.error(error);
      res.status(500).json({ error: 'Internal Server Error' });
    }
  });
  
  // Function to generate a unique port within the specified range
  async function generateUniquePort(min, max) {
    let port;
    do {
      port = Math.floor(Math.random() * (max - min + 1)) + min;
    } while (await isPortInUse(port));
  
    return port;
  }
  
  // Function to check if a port is already in use
  async function isPortInUse(port) {
    const existingDocument = await Document.findOne({
      $or: [
        { portVue: port },
        { portFlask: port },
        { portApache: port },
      ],
    });
  
    return !!existingDocument;
  }

  //Get a specific document
app.get('/document/:documentId', async (req, res) => {
    try {
      const { documentId } = req.params;
  
      // Find the document by ID
      const document = await Document.findById(documentId);
  
      if (!document) {
        return res.status(404).json({ error: 'Document not found' });
      }
  
      res.status(200).json(document);
    } catch (error) {
      console.error(error);
      res.status(500).json({ error: 'Internal Server Error' });
    }
  });

  

  // Delete a document from a customer
app.delete('/delete-document/:customerId/:documentId', async (req, res) => {
    try {
      const { customerId, documentId } = req.params;
  
      // Find the customer by ID
      const customer = await Customer.findById(customerId);
  
      if (!customer) {
        return res.status(404).json({ error: 'Customer not found' });
      }
  
      // Find the document by ID
      const documentIndex = customer.documents.findIndex(doc => doc._id == documentId);
  
      if (documentIndex === -1) {
        return res.status(404).json({ error: 'Document not found' });
      }
  
      // Remove the document from the customer's array
      const deletedDocument = customer.documents.splice(documentIndex, 1)[0];
  
      // Save the updated customer to the database
      await customer.save();
  
      res.status(200).json({ message: 'Document deleted successfully', deletedDocument });
    } catch (error) {
      console.error(error);
      res.status(500).json({ error: 'Internal Server Error' });
    }
  });


//Allow to update the customer name
app.put('/update-customer/:id', async (req, res) => {
    try {
      const { id } = req.params;
      const { name } = req.body;
  
      // Find the customer by ID
      const customer = await Customer.findById(id);
  
      if (!customer) {
        return res.status(404).json({ error: 'Customer not found' });
      }
  
      // Update the customer's name
      customer.name = name;
  
      // Save the updated customer to the database
      await customer.save();
  
      res.status(200).json(customer);
    } catch (error) {
      console.error(error);
      res.status(500).json({ error: 'Internal Server Error' });
    }
  });

//Allow to update the document name
app.put('/update-document/:customerId/:documentId', async (req, res) => {
    try {
      const { customerId, documentId } = req.params;
      const { name } = req.body;
  
      // Find the customer by ID
      const customer = await Customer.findById(customerId);
  
      if (!customer) {
        return res.status(404).json({ error: 'Customer not found' });
      }
  
      // Find the document by ID
      const document = customer.documents.find(doc => doc._id == documentId);
  
      if (!document) {
        return res.status(404).json({ error: 'Document not found' });
      }
  
      // Update the document's name
      document.name = name;
  
      // Save the updated customer to the database
      await customer.save();
  
      res.status(200).json(document);
    } catch (error) {
      console.error(error);
      res.status(500).json({ error: 'Internal Server Error' });
    }
  });
  




// Start the server
app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
  });
  