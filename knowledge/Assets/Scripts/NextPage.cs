using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NextPage : MonoBehaviour
{
    public GameObject m_GameobjectPageBack;
    public int m_rotateAngle;

    // Update is called once per frame
    void Update()
    {
        transform.rotation = Quaternion.Euler(new Vector3(0, 0, m_rotateAngle));
        m_GameobjectPageBack.transform.rotation = Quaternion.Euler(0, 0, 0);
    }
}
