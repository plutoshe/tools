using System.Collections;
using System.Collections.Generic;
using System.IO;
using System;
using UnityEngine;
using YamlDotNet.Serialization;

public class DataManager : MonoBehaviour
{
    private string m_RecordCurrentModificationFilePath = "RecordCurrentModification.yaml";
    private string m_RecordDataStorageFilePath = "RecordDataStorage.yaml";
    private List<RecordInfo> m_reviewingRecords;
    private int m_currentReviewRecordID;

    private bool needReview(RecordInfo record)
    {
        return true;
    }

    private string GetDataPath(string filename)
    {
        return Path.Combine(Application.dataPath, Path.Combine("data", filename));
    }

    static public void Serializer<T>(string _filePath, T obj) 
    {
        StreamWriter yamlWriter = File.CreateText(_filePath);
        Serializer yamlSerializer = new Serializer();
        yamlSerializer.Serialize(yamlWriter, obj);
        yamlWriter.Close();
    }

    static public T Deserializer<T>(string _filePath) 
    {
        if (!File.Exists(_filePath))
        {
            throw new FileNotFoundException();
        }
        StreamReader yamlReader = File.OpenText(_filePath);
        Deserializer yamlDeserializer = new Deserializer();

        T info = yamlDeserializer.Deserialize<T>(yamlReader);
        yamlReader.Close();
        return info;
    }

    private RecordDataStorage GetRecordDataStorage()
    {
        string dataPath = GetDataPath(m_RecordDataStorageFilePath);
        return Deserializer<RecordDataStorage>(dataPath);
    }


    private void Awake()
    {

        RecordDataStorage info = GetRecordDataStorage();

        m_reviewingRecords = new List<RecordInfo>();
        for (int i = 0; i < info.RecordList.Count; i++)
        {
            if (needReview(info.RecordList[i]))
            {
                m_reviewingRecords.Add(info.RecordList[i]);
            }
        }
        m_currentReviewRecordID = 0;
        m_reviewingRecords[0].CreateDate = DateTime.Now;
        SaveReviewingRecords();
    }

    public void SaveReviewingRecords()
    {
        var reviewingPath = GetDataPath(m_RecordCurrentModificationFilePath);
        Serializer(reviewingPath, new RecordDataStorage(m_reviewingRecords));

    }

    public void ReviewNextRecord()
    {
        m_currentReviewRecordID++;
    }

    public void ModifyCurrentRecord(RecordInfo modifiedRecord)
    {
        m_reviewingRecords[m_currentReviewRecordID] = modifiedRecord;
        SaveReviewingRecords();
    }

    public void UpdateCurrentReviewingRecord(ReviewingStatus status)
    {
        switch (status)
        {
            case ReviewingStatus.Forget:break;
            case ReviewingStatus.Remember: break;
        }
        ReviewNextRecord();
    }
    
}
