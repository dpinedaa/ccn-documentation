import { createStore } from 'vuex'

export default createStore({
  state: {
    sectionNumber: localStorage.getItem('sectionNumber') || '',
    objectId: localStorage.getItem('objectId') || '', // Add the objectId state
    filename:   localStorage.getItem('filename') || '', // Add the filename state
    fileContentText: localStorage.getItem('fileContentText') || '', // Add the filecontent state
    fileContentCSV: localStorage.getItem('fileContentCSV') || '', // Add the filecontent state


  },
  getters: {
    sectionNumber(state){
      return state.sectionNumber;
    },
    objectId(state) {
      return state.objectId; // Add the getter for objectId
    },
    filename(state) {
      return state.filename; // Add the getter for filename
    },
    fileContentText(state) {
      return state.fileContentText; // Add the getter for filecontent
    },
    fileContentCSV(state) {
      return state.fileContentCSV; // Add the getter for filecontent
    },
    
  },
  mutations: {
    setSectionNumber(state, sectionNumber){
      state.sectionNumber = sectionNumber;
      localStorage.setItem('sectionNumber',sectionNumber);
    },
    setObjectId(state, objectId) { // Add the mutation to set the objectId
      state.objectId = objectId;
      localStorage.setItem('objectId', objectId);
    },
    setFilename(state, filename) { // Add the mutation to set the filename
      state.filename = filename;
      localStorage.setItem('filename', filename);
    },
    setFilecontent(state, filecontent) { // Add the mutation to set the filecontent
      state.filecontent = filecontent;
      localStorage.setItem('filecontent', filecontent);
    },
    setFileContentText(state, fileContentText) { // Add the mutation to set the filecontent
      state.fileContentText = fileContentText;
      localStorage.setItem('fileContentText', fileContentText);
    },
    setFileContentCSV(state, fileContentCSV) { // Add the mutation to set the filecontent
      state.fileContentCSV = fileContentCSV;
      localStorage.setItem('fileContentCSV', fileContentCSV);
    },


  },
  actions: {
    setSectionNumber(context,sectionNumber){
      context.commit('sectionNumber',sectionNumber);
    },
    setObjectId(context, objectId) { // Add the action to set the objectId
      context.commit('setObjectId', objectId);
    },
    setFilename(context, filename) { // Add the action to set the filename
      context.commit('setFilename', filename);
    },
    setFilecontent(context, filecontent) { // Add the action to set the filecontent
      context.commit('setFilecontent', filecontent);
    },
    setFileContentText(context, fileContentText) { // Add the action to set the filecontent
      context.commit('setFileContentText', fileContentText);
    },
    setFileContentCSV(context, fileContentCSV) { // Add the action to set the filecontent
      context.commit('setFileContentCSV', fileContentCSV);
    },
    

  },
  modules: {
  }
})
