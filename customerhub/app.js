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
const port = process.env.PORT || 1502;

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


// Delete a customer and associated documents
app.delete('/customers/:id', async (req, res) => {
  try {
    const { id } = req.params;

    console.log(id);

    // Find the customer by ID
    const customer = await Customer.findById(id);

    if (!customer) {
      return res.status(404).json({ error: 'Customer not found' });
    }

    // Get document IDs associated with the customer
    const documentIds = customer.documents.map(doc => doc._id);

    // Delete the customer
    await Customer.findByIdAndDelete(id);

    // Delete associated documents from the document collection
    await Document.deleteMany({ _id: { $in: documentIds } });

    res.status(200).json({ message: 'Customer and associated documents deleted successfully' });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});
 









// Function to obtain portVue values
async function getAvailablePortVue() {
  try {
    // Get all documents
    const documents = await Document.find();

    for (let portVue = 2002; portVue <= 4000; portVue++) {
      // Check if the current portVue is available
      const isPortVueAvailable = documents.every(doc => {
        return portVue !== doc.portVue;
      });

      // If the portVue is available, return it
      if (isPortVueAvailable) {
        return portVue;
      }
    }

    // If no available portVue is found, you might want to handle this case
    throw new Error('No available portVue found between 2002 and 4000');
  } catch (error) {
    console.error(error);
    throw new Error('Error obtaining portVue values');
  }
}

// Add a document to a customer
app.post('/add-document/:customerId', async (req, res) => {
  try {
    const available = await getAvailablePortVue();
    console.log(available);

    const customerId = req.params.customerId;
    const { name } = req.body;

    // Find the customer by ID
    const foundCustomer = await Customer.findById(customerId);
    const customerName = foundCustomer.name;

    const portVue = available;
    const portFlask = available + 2000;
    const portApache = available + 4000;

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

    // Add the document to the customer
    customer.documents.push(document);

    // Save the updated customer to the database
    await customer.save();

    await document.save();

    res.status(201).json(document);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});












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

      // Delete the document from the overall documents collection
      await Document.findByIdAndDelete(documentId);

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

      console.log(id);  
  
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

    //get the document collection 
    const documents = await Document.find();
    console.log("Documents: ");
    console.log(documents);
    try {
      const { customerId, documentId } = req.params;
      const { name } = req.body;

      console.log(customerId);
      console.log(documentId);
      console.log(name);

      // Find the customer by ID
      const customer = await Customer.findById(customerId);

      console.log("Customer: " + customer);
  
      if (!customer) {
        return res.status(404).json({ error: 'Customer not found' });
      }
  
      // Find the document by ID
      const document = customer.documents.find(doc => doc._id == documentId);
      console.log("Document: " + document);
      
      if (!document) {
        return res.status(404).json({ error: 'Document not found' });
      }
  
      // Update the document's name
      document.name = name;
      document._id = customer.name + "-" + name;

  
      // Save the updated customer to the database
      await customer.save();

      let doc = await Document.findOne({ _id: documentId });
      const newID = customer.name + "-" + name;
      let newDoc = new Document({
        _id: newID,
        name: name,
        portVue: doc.portVue,
        portFlask: doc.portFlask,
        portApache: doc.portApache,
        customerName: doc.customerName
      });


      await newDoc.save();
      await Document.deleteOne({ _id: documentId });

  
      res.status(200).json(document);
    } catch (error) {
      console.error(error);
      res.status(500).json({ error: 'Internal Server Error' });
    }
  });
  







//Get all documents
app.get('/documents', async (req, res) => {

  // Call the function to get available portVue
  getAvailablePortVue();
    try {
      const documents = await Document.find();
      res.status(200).json(documents);

      // Iterate over the documents and print details
      documents.forEach(doc => {
        console.log(`Document ID: ${doc._id}`);
        console.log(`Name: ${doc.name}`);
        console.log(`PortVue: ${doc.portVue}`);
        console.log(`PortFlask: ${doc.portFlask}`);
        console.log(`PortApache: ${doc.portApache}`);
        console.log('------------------------');
    });
    } catch (error) {
      console.error(error);
      res.status(500).json({ error: 'Internal Server Error' });
    }
  });


  //Get specific customer
app.get('/customer/:customerId', async (req, res) => {
    try {
      const { customerId } = req.params;
  
      // Find the customer by ID
      const customer = await Customer.findById(customerId);
  
      if (!customer) {
        return res.status(404).json({ error: 'Customer not found' });
      }
  
      res.status(200).json(customer);
    } catch (error) {
      console.error(error);
      res.status(500).json({ error: 'Internal Server Error' });
    }
  }
);


// Start the server
app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
  });
  