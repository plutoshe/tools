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
    private ReviewingIndexing m_reviewingRecords;
    private RecordDataStorage m_recordDataBase;
    private int m_currentReviewRecordID;

    private bool needReview(RecordInfo record)
    {
        return DateTime.Compare(DateTime.Now, record.ReviewDate) > 0;
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
            return default;
            //throw new FileNotFoundException();
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
        m_recordDataBase = GetRecordDataStorage();
        if (m_recordDataBase == null)
        {
            m_recordDataBase = new RecordDataStorage();
        }

        m_reviewingRecords = new ReviewingIndexing();
        m_reviewingRecords.RecordIDNum = m_recordDataBase.RecordIDNum;
        foreach (KeyValuePair<int, RecordInfo> kv in m_recordDataBase.RecordDict)
        {
            if (needReview(kv.Value))
            {
                m_reviewingRecords.RecordList.Add(kv.Value);
            }
        }
        m_currentReviewRecordID = 0;
        SaveReviewingRecords();
    }

    public void SaveReviewingRecords()
    {
        var reviewingPath = GetDataPath(m_RecordCurrentModificationFilePath);
        Serializer(reviewingPath, m_reviewingRecords);

    }

    public void SaveRecordDataStorage()
    {
        var dataStoragePath = GetDataPath(m_RecordDataStorageFilePath);
        Serializer(dataStoragePath, m_recordDataBase);

    }

    public void ReviewNextRecord()
    {
        m_currentReviewRecordID++;
    }

    public void ModifyCurrentRecord(RecordInfo modifiedRecord)
    {
        m_reviewingRecords.RecordList[m_currentReviewRecordID] = modifiedRecord;
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

    public void AddNewRecord(RecordInfo record)
    {
        m_reviewingRecords.AddRecord(record);
        SaveReviewingRecords();
    }

    public void Update()
    {
        if (Input.GetKeyDown(KeyCode.P))
        {
            var a = new RecordInfo();
            var now = DateTime.Now;
            a.CreateDate = now;
            a.ReviewDate = new DateTime(now.Year, now.Month, now.Day).AddDays(1);
            a.Front = "a";
            a.Back = "b";
            AddNewRecord(a);
        }
        if (Input.GetKeyDown(KeyCode.L))
        {
            m_recordDataBase.CombineDerivedeReviewingIndexing(m_reviewingRecords);
            SaveRecordDataStorage();
        }
    }

}
