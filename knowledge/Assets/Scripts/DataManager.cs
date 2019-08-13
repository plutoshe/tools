using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;
using YamlDotNet.Serialization;

public class DataManager : MonoBehaviour
{
    public string m_RecordCurrentModificationFilePath = "RecordCurrentModification.yaml";
    public string m_RecordDataStorageFilePath = "RecordDataStorage.yaml";

    private void Awake()
    {
        string dataPath = Path.Combine(Application.dataPath, "data/" + m_RecordCurrentModificationFilePath);
        print(Application.dataPath);
        print(dataPath);
        if (!File.Exists(dataPath))
        {
            return;
        }

        StreamReader yamlReader = File.OpenText(dataPath);
        Deserializer yamlDeserializer = new Deserializer();
        RecordDataStorage info = yamlDeserializer.Deserialize<RecordDataStorage>(yamlReader);
        yamlReader.Close();

    }
}
