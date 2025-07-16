# MySQL · 引擎介绍 · Sphinx源码剖析（二）

**Date:** 2017/04
**Source:** http://mysql.taobao.org/monthly/2017/04/03/
**Images:** 1 images downloaded

---

数据库内核月报

 [
 # 数据库内核月报 － 2017 / 04
 ](/monthly/2017/04)

 * 当期文章

 MySQL · 源码分析 · MySQL 半同步复制数据一致性分析
* MYSQL · 新特性 · MySQL 8.0对Parser所做的改进
* MySQL · 引擎介绍 · Sphinx源码剖析（二）
* PgSQL · 特性分析 · checkpoint机制浅析
* MySQL · 特性分析 · common table expression
* PgSQL · 应用案例 · 逻辑订阅给业务架构带来了什么？
* MSSQL · 应用案例 · 基于内存优化表的列存储索引分析Web Access Log
* TokuDB · 捉虫动态 · MRR 导致查询失败
* HybridDB · 稳定性 · HybridDB如何优雅的处理Out Of Memery问题
* MySQL · 捉虫动态 · 5.7 mysql_upgrade 元数据锁等待

 ## MySQL · 引擎介绍 · Sphinx源码剖析（二） 
 Author: 雕梁 

 在本节中，我将会介绍索引文件sph的生成，从上一节我们得知sph文件保存了Sphinx的索引元信息以及一些索引相关的配置信息

## SPH文件生成

先来看代码，其中sph文件的生成是在CSphIndex_VLN::WriteHeader这个函数中:

` bool CSphIndex_VLN::WriteHeader ( const BuildHeader_t & tBuildHeader, CSphWriter & fdInfo ) const
{
 // version
 fdInfo.PutDword ( INDEX_MAGIC_HEADER );
 fdInfo.PutDword ( INDEX_FORMAT_VERSION );

 // bits
 fdInfo.PutDword ( USE_64BIT );

 // docinfo
 fdInfo.PutDword ( m_tSettings.m_eDocinfo );

 // schema
 WriteSchema ( fdInfo, m_tSchema );

 // min doc
 fdInfo.PutOffset ( tBuildHeader.m_uMinDocid ); // was dword in v.1
 if ( m_tSettings.m_eDocinfo==SPH_DOCINFO_INLINE )
 fdInfo.PutBytes ( tBuildHeader.m_pMinRow, m_tSchema.GetRowSize()*sizeof(CSphRowitem) );

 // wordlist checkpoints
 fdInfo.PutOffset ( tBuildHeader.m_iDictCheckpointsOffset );
 fdInfo.PutDword ( tBuildHeader.m_iDictCheckpoints );
 fdInfo.PutByte ( tBuildHeader.m_iInfixCodepointBytes );
 fdInfo.PutDword ( (DWORD)tBuildHeader.m_iInfixBlocksOffset );
 fdInfo.PutDword ( tBuildHeader.m_iInfixBlocksWordsSize );

 // index stats
 fdInfo.PutDword ( (DWORD)tBuildHeader.m_iTotalDocuments ); // FIXME? we don't expect over 4G docs per just 1 local index
 fdInfo.PutOffset ( tBuildHeader.m_iTotalBytes );
 fdInfo.PutDword ( tBuildHeader.m_iTotalDups );

 // index settings
 SaveIndexSettings ( fdInfo, m_tSettings );

 // tokenizer info
 assert ( m_pTokenizer );
 SaveTokenizerSettings ( fdInfo, m_pTokenizer, m_tSettings.m_iEmbeddedLimit );

 // dictionary info
 assert ( m_pDict );
 SaveDictionarySettings ( fdInfo, m_pDict, false, m_tSettings.m_iEmbeddedLimit );

 fdInfo.PutDword ( tBuildHeader.m_uKillListSize );
 fdInfo.PutOffset ( tBuildHeader.m_iMinMaxIndex );

 // field filter info
 SaveFieldFilterSettings ( fdInfo, m_pFieldFilter );

 // average field lengths
 if ( m_tSettings.m_bIndexFieldLens )
 ARRAY_FOREACH ( i, m_tSchema.m_dFields )
 fdInfo.PutOffset ( m_dFieldLens[i] );

 return true;
}
`
然后按顺序来解释下每一项字段的含义.

* 前两个字段INDEX_MAGIC_HEADER和INDEX_FORMAT_VERSION分别是magic number和索引版本号
* 第三个字段USE_64BIT表示是否使用64位的document和word id(默认是使用).
* 然后是写入docinfo,这个字段也就是配置中的docinfo字段(index block中)
* 接下来将会写入schema，也就是索引的schema信息，比如当前索引的字段名，当前需要建立的属性名等等.

```
 void WriteSchema ( CSphWriter & fdInfo, const CSphSchema & tSchema )
{
 // schema
 fdInfo.PutDword ( tSchema.m_dFields.GetLength() );
 ARRAY_FOREACH ( i, tSchema.m_dFields )
 WriteSchemaColumn ( fdInfo, tSchema.m_dFields[i] );

 fdInfo.PutDword ( tSchema.GetAttrsCount() );
 for ( int i=0; i<tSchema.GetAttrsCount(); i++ )
 WriteSchemaColumn ( fdInfo, tSchema.GetAttr(i) );
}

```

* 然后是写入当前索引集的最小doc id(m_uMinDocid)
* 接下来是根据docinfo(也就是属性存储)的配置来选择是否写入行信息(当docinfo为inline的话，表示attribute value 将会存储在spd文件中).
* 然后是写入wordlist的checkpoint.
* 然后是索引的统计信息(m_iTotalDocuments/m_iTotalBytes/m_iTotalDups).
* 接下来是写入对应的索引配置信息

```
void SaveIndexSettings ( CSphWriter & tWriter, const CSphIndexSettings & tSettings )
{
 tWriter.PutDword ( tSettings.m_iMinPrefixLen );
 tWriter.PutDword ( tSettings.m_iMinInfixLen );
 tWriter.PutDword ( tSettings.m_iMaxSubstringLen );
 tWriter.PutByte ( tSettings.m_bHtmlStrip ? 1 : 0 );
 tWriter.PutString ( tSettings.m_sHtmlIndexAttrs.cstr () );
 tWriter.PutString ( tSettings.m_sHtmlRemoveElements.cstr () );
 tWriter.PutByte ( tSettings.m_bIndexExactWords ? 1 : 0 );
 tWriter.PutDword ( tSettings.m_eHitless );
 tWriter.PutDword ( tSettings.m_eHitFormat );
 tWriter.PutByte ( tSettings.m_bIndexSP );
 tWriter.PutString ( tSettings.m_sZones );
 tWriter.PutDword ( tSettings.m_iBoundaryStep );
 tWriter.PutDword ( tSettings.m_iStopwordStep );
 tWriter.PutDword ( tSettings.m_iOvershortStep );
 tWriter.PutDword ( tSettings.m_iEmbeddedLimit );
 tWriter.PutByte ( tSettings.m_eBigramIndex );
 tWriter.PutString ( tSettings.m_sBigramWords );
 tWriter.PutByte ( tSettings.m_bIndexFieldLens );
 tWriter.PutByte ( tSettings.m_eChineseRLP );
 tWriter.PutString ( tSettings.m_sRLPContext );
 tWriter.PutString ( tSettings.m_sIndexTokenFilter );
}

```

* 写入对应的tokenizer的配置信息,

```
void SaveTokenizerSettings ( CSphWriter & tWriter, ISphTokenizer * pTokenizer, int iEmbeddedLimit )
{
 assert ( pTokenizer );

 const CSphTokenizerSettings & tSettings = pTokenizer->GetSettings ();
 tWriter.PutByte ( tSettings.m_iType );
 tWriter.PutString ( tSettings.m_sCaseFolding.cstr () );
 tWriter.PutDword ( tSettings.m_iMinWordLen );

 bool bEmbedSynonyms = pTokenizer->GetSynFileInfo ().m_uSize<=(SphOffset_t)iEmbeddedLimit;
 tWriter.PutByte ( bEmbedSynonyms ? 1 : 0 );
 if ( bEmbedSynonyms )
 pTokenizer->WriteSynonyms ( tWriter );

 tWriter.PutString ( tSettings.m_sSynonymsFile.cstr () );
 WriteFileInfo ( tWriter, pTokenizer->GetSynFileInfo () );
 tWriter.PutString ( tSettings.m_sBoundary.cstr () );
 tWriter.PutString ( tSettings.m_sIgnoreChars.cstr () );
 tWriter.PutDword ( tSettings.m_iNgramLen );
 tWriter.PutString ( tSettings.m_sNgramChars.cstr () );
 tWriter.PutString ( tSettings.m_sBlendChars.cstr () );
 tWriter.PutString ( tSettings.m_sBlendMode.cstr () );
}

```

* 写入dictionary的配置信息(比如stop word之类).

```
void SaveDictionarySettings ( CSphWriter & tWriter, CSphDict * pDict, bool bForceWordDict, int iEmbeddedLimit )
{
 assert ( pDict );
 const CSphDictSettings & tSettings = pDict->GetSettings ();

 tWriter.PutString ( tSettings.m_sMorphology.cstr () );
.............................

 bool bEmbedStopwords = uTotalSize<=(SphOffset_t)iEmbeddedLimit;
 tWriter.PutByte ( bEmbedStopwords ? 1 : 0 );
 if ( bEmbedStopwords )
 pDict->WriteStopwords ( tWriter );

 tWriter.PutString ( tSettings.m_sStopwords.cstr () );
 tWriter.PutDword ( dSWFileInfos.GetLength () );
 ARRAY_FOREACH ( i, dSWFileInfos )
 {
 tWriter.PutString ( dSWFileInfos[i].m_sFilename.cstr () );
 WriteFileInfo ( tWriter, dSWFileInfos[i] );
 }

 const CSphVector <CSphSavedFile> & dWFFileInfos = pDict->GetWordformsFileInfos ();
 uTotalSize = 0;
 ARRAY_FOREACH ( i, dWFFileInfos )
 uTotalSize += dWFFileInfos[i].m_uSize;

 bool bEmbedWordforms = uTotalSize<=(SphOffset_t)iEmbeddedLimit;
 tWriter.PutByte ( bEmbedWordforms ? 1 : 0 );
 if ( bEmbedWordforms )
 pDict->WriteWordforms ( tWriter );

 tWriter.PutDword ( dWFFileInfos.GetLength() );
 ARRAY_FOREACH ( i, dWFFileInfos )
 {
 tWriter.PutString ( dWFFileInfos[i].m_sFilename.cstr() );
 WriteFileInfo ( tWriter, dWFFileInfos[i] );
 }

 tWriter.PutDword ( tSettings.m_iMinStemmingLen );
 tWriter.PutByte ( tSettings.m_bWordDict || bForceWordDict );
 tWriter.PutByte ( tSettings.m_bStopwordsUnstemmed );
 tWriter.PutString ( pDict->GetMorphDataFingerprint() );
}

```

* 然后是写入killlist的size（m_uKillListSize)
* 写入m_iMinMaxIndex，这个选项也就是表示document size.

```
 CSphFixedVector<CSphRowitem> dMinRow ( tNewSchema.GetRowSize() );
 ...............
 int iNewStride = DOCINFO_IDSIZE + tNewSchema.GetRowSize();

 int64_t iNewMinMaxIndex = m_iDocinfo * iNewStride;
..............................
 tBuildHeader.m_iMinMaxIndex = iNewMinMaxIndex;

```

* 写入regex相关配置(regexp_filter)

```
void SaveFieldFilterSettings ( CSphWriter & tWriter, ISphFieldFilter * pFieldFilter )
{
 if ( !pFieldFilter )
 {
 tWriter.PutDword ( 0 );
 return;
 }

 CSphFieldFilterSettings tSettings;
 pFieldFilter->GetSettings ( tSettings );

 tWriter.PutDword ( tSettings.m_dRegexps.GetLength() );
 ARRAY_FOREACH ( i, tSettings.m_dRegexps )
 tWriter.PutString ( tSettings.m_dRegexps[i] );

 tWriter.PutByte(1); // deprecated utf8 flag
}

```

* 最后是写入对应的schema field长度.

 阅读： - 

[![知识共享许可协议](.img/8232d49bd3e9_88x31.png)](http://creativecommons.org/licenses/by-nc-sa/3.0/)
本作品采用[知识共享署名-非商业性使用-相同方式共享 3.0 未本地化版本许可协议](http://creativecommons.org/licenses/by-nc-sa/3.0/)进行许可。

 [

 ](#0)